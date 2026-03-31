import pandas as pd
import json
from functools import lru_cache
from config.database import db
from geopy.distance import geodesic

class CoralDataService:
    def get_locality_data(self):
        query = "SELECT locality_id, name, coords_local FROM data_coralsol_locality"
        df = pd.read_sql(query, db.engine)

        # Parse JSON coordinates with error handling
        def parse_coords(val):
            try:
                coords = json.loads(val)
                if coords and isinstance(coords[0], list):
                    return coords[0]
            except Exception:
                return [None, None]
            return [None, None]

        df[['LATITUDE', 'LONGITUDE']] = df['coords_local'].apply(parse_coords).apply(pd.Series)
        return df  # <-- Do NOT drop 'coords_local'

    def get_dafor_data(self, start_date=None, end_date=None):
        query = "SELECT Dafor_id, Locality_id, Dafor_coords, Date, Dafor_value FROM data_coralsol_dafor"
        df = pd.read_sql(query, db.engine)
        df.columns = df.columns.str.lower()  # Standardize to lowercase
        if start_date and end_date:
            df['date'] = pd.to_datetime(df['date'])
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        return df

    def get_dafor_spatial_data(self, start_date=None, end_date=None):
        """
        Spatialize DAFOR scores along locality boundaries with 100m resolution.
        1. Split each monitoring transect into 100m segments with averaged DAFOR scores
        2. Split locality boundaries into 100m segments
        3. Overlay monitoring segments onto locality segments and average

        Uses caching to improve performance on repeated calls.
        """
        # Convert dates to strings for cache key
        cache_key = (str(start_date) if start_date else None, str(end_date) if end_date else None)
        return self._get_dafor_spatial_data_cached(cache_key)

    @lru_cache(maxsize=32)
    def _get_dafor_spatial_data_cached(self, cache_key):
        """Cached implementation of spatial DAFOR processing"""
        # Extract dates from cache key
        start_date = pd.to_datetime(cache_key[0]) if cache_key[0] and cache_key[0] != 'None' else None
        end_date = pd.to_datetime(cache_key[1]) if cache_key[1] and cache_key[1] != 'None' else None
        import numpy as np
        from scipy.spatial import cKDTree

        # Get locality data with coordinates
        df_locality = self.get_locality_data()

        # Get DAFOR data
        df_dafor = self.get_dafor_data(start_date, end_date)
        print(f"[DAFOR SPATIAL] Processing {len(df_dafor)} DAFOR records...")

        # Step 1: Process each monitoring transect into 20m segments
        monitoring_segments = []

        for _, row in df_dafor.iterrows():
            try:
                coords = json.loads(row['dafor_coords'])
                dafor_values = [pd.to_numeric(i, errors='coerce') for i in str(row['dafor_value']).split(',')]
                dafor_values = [v for v in dafor_values if not pd.isna(v)]

                if not coords or len(coords) < 2 or not dafor_values:
                    continue

                # Calculate cumulative distances
                cumulative_dist = [0]
                for i in range(len(coords) - 1):
                    dist = geodesic(coords[i], coords[i+1]).meters
                    cumulative_dist.append(cumulative_dist[-1] + dist)

                total_length = cumulative_dist[-1]
                if total_length == 0:
                    continue

                # Create 100m segments along this transect
                num_segments = max(1, int(total_length / 100))
                segment_length = total_length / num_segments
                values_per_segment = max(1, len(dafor_values) // num_segments)

                for seg_idx in range(num_segments):
                    start_dist = seg_idx * segment_length
                    end_dist = min((seg_idx + 1) * segment_length, total_length)

                    # Get DAFOR values for this segment
                    start_val_idx = seg_idx * values_per_segment
                    end_val_idx = min((seg_idx + 1) * values_per_segment, len(dafor_values))
                    segment_dafor_values = dafor_values[start_val_idx:end_val_idx]

                    if not segment_dafor_values:
                        continue

                    # Use weighted average - weight by number of observations (effort)
                    avg_dafor = np.mean(segment_dafor_values)
                    effort = len(segment_dafor_values)  # number of minutes

                    # Get midpoint coordinates
                    mid_dist = (start_dist + end_dist) / 2
                    mid_point = self._interpolate_point_on_line(coords, cumulative_dist, mid_dist)

                    if mid_point:
                        monitoring_segments.append({
                            'locality_id': row['locality_id'],
                            'lat': mid_point[0],
                            'lon': mid_point[1],
                            'dafor_score': avg_dafor,
                            'effort': effort  # track effort for weighting
                        })

            except Exception as e:
                print(f"[DAFOR SPATIAL] Error processing transect: {e}")
                continue

        print(f"[DAFOR SPATIAL] Created {len(monitoring_segments)} 100m monitoring segments")

        # Step 2: Process each locality into 100m segments and overlay monitoring data
        locality_segments = []

        for _, loc_row in df_locality.iterrows():
            try:
                coords = json.loads(loc_row['coords_local'])
                if not coords or len(coords) < 2:
                    continue

                # Get monitoring segments for this locality
                loc_monitoring = [s for s in monitoring_segments if s['locality_id'] == loc_row['locality_id']]

                if not loc_monitoring:
                    continue

                # Build KDTree for fast spatial lookup
                monitoring_coords = np.array([[s['lat'], s['lon']] for s in loc_monitoring])
                monitoring_scores = np.array([s['dafor_score'] for s in loc_monitoring])
                monitoring_efforts = np.array([s['effort'] for s in loc_monitoring])
                tree = cKDTree(monitoring_coords)

                # Calculate cumulative distances along locality boundary
                cumulative_dist = [0]
                for i in range(len(coords) - 1):
                    dist = geodesic(coords[i], coords[i+1]).meters
                    cumulative_dist.append(cumulative_dist[-1] + dist)

                total_length = cumulative_dist[-1]
                if total_length == 0:
                    continue

                # Create 100m segments along locality boundary
                num_segments = max(1, int(total_length / 100))

                for seg_idx in range(num_segments):
                    start_dist = seg_idx * 100
                    end_dist = min((seg_idx + 1) * 100, total_length)

                    # Get start and end points
                    start_point = self._interpolate_point_on_line(coords, cumulative_dist, start_dist)
                    end_point = self._interpolate_point_on_line(coords, cumulative_dist, end_dist)

                    if not start_point or not end_point:
                        continue

                    # Find nearby monitoring segments (within 50m radius)
                    mid_point = [(start_point[0] + end_point[0]) / 2, (start_point[1] + end_point[1]) / 2]

                    # Query nearby points (0.0005 degrees ≈ 50m)
                    indices = tree.query_ball_point(mid_point, r=0.0005)

                    # Calculate DAFOR score (keep all segments, even with 0)
                    if indices:
                        # Use WEIGHTED AVERAGE - weight by effort (number of minutes)
                        nearby_scores = monitoring_scores[indices]
                        nearby_efforts = monitoring_efforts[indices]

                        # Weighted average: Σ(score × effort) / Σ(effort)
                        total_effort = np.sum(nearby_efforts)
                        if total_effort > 0:
                            weighted_score = np.sum(nearby_scores * nearby_efforts) / total_effort
                        else:
                            weighted_score = np.mean(nearby_scores)
                    else:
                        # No monitoring data nearby - assign 0 (absent)
                        weighted_score = 0.0

                    # Keep all segments regardless of score
                    locality_segments.append({
                        'locality_id': loc_row['locality_id'],
                        'name': loc_row['name'],
                        'start_lat': start_point[0],
                        'start_lon': start_point[1],
                        'end_lat': end_point[0],
                        'end_lon': end_point[1],
                        'dafor_score': weighted_score
                    })

            except Exception as e:
                print(f"[DAFOR SPATIAL] Error processing locality {loc_row.get('name')}: {e}")
                continue

        print(f"[DAFOR SPATIAL] Created {len(locality_segments)} locality segments")
        return pd.DataFrame(locality_segments)

    def _interpolate_point_on_line(self, coords, cumulative_dist, target_dist):
        """
        Interpolate a point at a specific distance along a polyline.
        Returns [lat, lon] at the target distance.
        """
        # Find which segment the target distance falls in
        for i in range(len(cumulative_dist) - 1):
            if cumulative_dist[i] <= target_dist <= cumulative_dist[i+1]:
                # Interpolate within this segment
                seg_start_dist = cumulative_dist[i]
                seg_end_dist = cumulative_dist[i+1]
                seg_length = seg_end_dist - seg_start_dist

                if seg_length == 0:
                    return coords[i]

                # How far along this segment?
                fraction = (target_dist - seg_start_dist) / seg_length

                # Interpolate coordinates
                start_lat, start_lon = coords[i]
                end_lat, end_lon = coords[i+1]

                interp_lat = start_lat + (end_lat - start_lat) * fraction
                interp_lon = start_lon + (end_lon - start_lon) * fraction

                return [interp_lat, interp_lon]

        # If target_dist is beyond the line, return the last point
        return coords[-1]

    def calculate_locality_length(self, coords_local):
        """Calculate the length of a locality based on its coordinates."""

        try:
            coords = json.loads(coords_local)
            if not coords or len(coords) < 2:
                return 0
            return sum(
                geodesic(coords[i], coords[i+1]).meters
                for i in range(len(coords)-1)
            )
        except Exception:
            return 0

    def calculate_dafor_length(self, dafor_coords):
        """Calculate the length (in meters) of a DAFOR line from its coordinates."""
        try:
            coords = json.loads(dafor_coords)
            if not coords or len(coords) < 2:
                return 0
            return sum(
                geodesic(coords[i], coords[i+1]).meters
                for i in range(len(coords)-1)
            )
        except Exception:
            return 0

    def get_dpue_by_locality(self, start_date=None, end_date=None):
        """Calculate DPUE (Detections Per Unit Effort) by locality within a date range."""

        # Fetch data
        df_locality = self.get_locality_data()
        df_dafor = self.get_dafor_data(start_date, end_date)

        # Calculate locality length
        df_locality['locality_length_m'] = df_locality['coords_local'].apply(self.calculate_locality_length)
        df_locality['Uni100m'] = df_locality['locality_length_m'] / 100

        # Process dafor_value
        df_dafor['dafor_value'] = df_dafor['dafor_value'].apply(
            lambda x: [pd.to_numeric(i, errors='coerce') for i in str(x).split(',')]
        )
        df_dafor = df_dafor.explode('dafor_value')
        df_dafor['dafor_value'] = pd.to_numeric(df_dafor['dafor_value'], errors='coerce')

        # Group by locality
        grouped = df_dafor.groupby('locality_id')
        df_dpue = grouped.agg(
            Ndetec=('dafor_value', lambda x: (x > 0).sum()),
            Nmin=('dafor_value', 'count')
        ).reset_index()
        df_dpue['Nhoras'] = df_dpue['Nmin'] / 60

        # Merge with locality data
        df_dpue = df_dpue.merge(df_locality[['locality_id', 'name', 'Uni100m']], left_on='locality_id', right_on='locality_id', how='left')
        df_dpue['DPUE'] = df_dpue['Ndetec'] / (df_dpue['Nhoras'] * df_dpue['Uni100m'])

        return df_dpue

    def get_raiw_by_locality(self, start_date=None, end_date=None):
        """
        Calculate RAI-W (Relative Abundance Index - Weighted) by locality within a date range.
        Raw formula: RAI-W_raw = sum_i w(s_i) / (N_hours × Uni100m)
        Where weights are: w(10)=1.00, w(8)=0.8, w(6)=0.6, w(4)=0.10, w(2)=0.04, w(0)=0

        To keep dashboard visualization in the DAFOR-like 0-10 range, this method returns
        a normalized score in `RAIW`:
            RAIW = 10 * (sum_i w(s_i) / Nmin)
        and also exposes the effort-normalized raw value in `RAIW_raw`.
        """
        # Define weight mapping
        weight_map = {
            10: 1.00,
            8: 0.80,
            6: 0.60,
            4: 0.10,
            2: 0.04,
            0: 0.00
        }

        # Fetch data
        df_locality = self.get_locality_data()
        df_dafor = self.get_dafor_data(start_date, end_date)

        # Calculate locality length
        df_locality['locality_length_m'] = df_locality['coords_local'].apply(self.calculate_locality_length)
        df_locality['Uni100m'] = df_locality['locality_length_m'] / 100

        # Process dafor_value - split comma-separated values and explode
        df_dafor['dafor_value'] = df_dafor['dafor_value'].apply(
            lambda x: [pd.to_numeric(i, errors='coerce') for i in str(x).split(',')]
        )
        df_dafor = df_dafor.explode('dafor_value')
        df_dafor['dafor_value'] = pd.to_numeric(df_dafor['dafor_value'], errors='coerce')

        # Apply weight mapping
        df_dafor['weight'] = df_dafor['dafor_value'].map(weight_map).fillna(0)

        # Group by locality and sum weights
        grouped = df_dafor.groupby('locality_id')
        df_raiw = grouped.agg(
            weight_sum=('weight', 'sum'),
            Nmin=('dafor_value', 'count')
        ).reset_index()
        df_raiw['Nhoras'] = df_raiw['Nmin'] / 60

        # Merge with locality data
        df_raiw = df_raiw.merge(
            df_locality[['locality_id', 'name', 'Uni100m']],
            left_on='locality_id',
            right_on='locality_id',
            how='left'
        )

        # Calculate raw effort-normalized RAI-W (can exceed 10 depending on locality size/effort).
        denominator = df_raiw['Nhoras'] * df_raiw['Uni100m']
        df_raiw['RAIW_raw'] = df_raiw['weight_sum'] / denominator

        # Dashboard-normalized weighted score in the 0-10 range.
        df_raiw['RAIW'] = (10 * (df_raiw['weight_sum'] / df_raiw['Nmin'])).clip(lower=0, upper=10)

        return df_raiw

    def get_dafor_value_histogram_data(self, start_date=None, end_date=None):
        """
        Prepares DAFOR values for histogram plotting (density of values in the DAFOR scale 1-10).
        Args:
            start_date (str or datetime, optional): The start date for filtering the data. Defaults to None.
            end_date (str or datetime, optional): The end date for filtering the data. Defaults to None.
        Returns:
            pandas.Series: A Series of all DAFOR values (flattened, numeric, NaNs dropped).
        """
        df_dafor = self.get_dafor_data(start_date, end_date)
        # Split and flatten dafor_value column
        df_dafor['dafor_value'] = df_dafor['dafor_value'].apply(
            lambda x: [pd.to_numeric(i, errors='coerce') for i in str(x).split(',')]
        )
        values = pd.to_numeric(pd.Series([v for sublist in df_dafor['dafor_value'] for v in sublist]), errors='coerce')
        values = values.dropna()
        # Optionally filter to 1-10 range
        values = values[(values >= 0) & (values <= 10)]
        return values


    def get_sum_of_dafor_by_locality(self, start_date=None, end_date=None):
        """
        Calculates the sum of DAFOR values by locality and date within an optional date range.
        Args:
            start_date (str or datetime, optional): The start date for filtering the data. Defaults to None.
            end_date (str or datetime, optional): The end date for filtering the data. Defaults to None.
        Returns:
            pandas.DataFrame: A DataFrame with columns ['locality_id', 'date', 'DAFOR'], where
            'DAFOR' is the sum of DAFOR values for each locality and date within the specified range.
        """
        # Fetch locality and DAFOR data
        df_locality = self.get_locality_data()
        df_dafor_sum = self.get_dafor_data(start_date, end_date)

        df_dafor_sum['dafor_value'] = df_dafor_sum['dafor_value'].apply(
            lambda x: [pd.to_numeric(i, errors='coerce') for i in str(x).split(',')]
        )
        df_dafor_sum = df_dafor_sum.explode('dafor_value')
        df_dafor_sum['dafor_value'] = pd.to_numeric(df_dafor_sum['dafor_value'], errors='coerce')

        # Group by locality and date
        df_dafor_sum = df_dafor_sum.groupby(['locality_id', 'date']).agg(
            DAFOR=('dafor_value', 'sum')
        ).reset_index()

        # Merge with locality data
        df_dafor_sum = df_dafor_sum.merge(df_locality[['locality_id', 'name']], left_on='locality_id', right_on='locality_id', how='left')

        # Fill NaN values in DAFOR with 0
        df_dafor_sum['DAFOR'] = df_dafor_sum['DAFOR'].fillna(0)

        return df_dafor_sum[['locality_id', 'name', 'date', 'DAFOR']]


    def get_occurrences_data(self, start_date=None, end_date=None):
        """
        Fetches occurrence data related to the Coral-Sol project, including locality names.
        """
        query = "SELECT Locality_id, Occurrence_id, Spot_Coords, Date, Depth, Access, Geomorphology, Subaquatica_photo, Superficie_photo FROM data_coralsol_occurrence"
        df = pd.read_sql(query, db.engine)
        df.columns = df.columns.str.lower()  # Standardize to lowercase

        df['date'] = pd.to_datetime(df['date'], dayfirst=True)

        if start_date and end_date:
            df_occ = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        else:
            df_occ = df

        # Merge with locality names
        df_locality = self.get_locality_data()[['locality_id', 'name']]
        df_occ = df_occ.merge(df_locality, on='locality_id', how='left')

        BASE_URL = "https://api-bd.institutohorus.org.br/api"
        for col in ["subaquatica_photo", "superficie_photo"]:
            df_occ[col] = df_occ.apply(
                lambda row: f"{BASE_URL}/Upload/UploadImageCoralSol/{row['occurrence_id']}/{row[col]}"
                if pd.notnull(row[col]) and str(row[col]).strip() != "" else None,
                axis=1
            )

        print(df_occ[['occurrence_id', 'name', 'subaquatica_photo', 'superficie_photo']].head(10))  # Debugging

        # Reorder columns to include 'name' after 'locality_id'
        return df_occ[['locality_id', 'name', 'occurrence_id', 'spot_coords', 'date', 'depth', 'access', 'geomorphology', 'subaquatica_photo', 'superficie_photo']]

    def get_management_data(self, start_date=None, end_date=None):
        """
        Fetches management data .
        Returns:
            pandas.DataFrame: A DataFrame containing management data.
        """
        query = "SELECT management_id, Locality_id, Management_coords, Date, Observer, Depth, Number_of_divers, Number_of_cylinders, Method, Managed_mass_kg, Observation, occurrences_managed FROM data_coralsol_management"
        df = pd.read_sql(query, db.engine)
        df.columns = df.columns.str.lower()

        df['date'] = pd.to_datetime(df['date'], dayfirst=True)

        if start_date and end_date:
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        return df[['management_id', 'locality_id', 'management_coords', 'date', 'observer', 'depth', 'number_of_divers', 'number_of_cylinders', 'method', 'managed_mass_kg', 'observation', 'occurrences_managed']]

    def get_days_since_last_management(self, start_date=None, end_date=None):
        query = "SELECT Locality_id, Date, Observation FROM data_coralsol_management"
        df = pd.read_sql(query, db.engine)
        df.columns = df.columns.str.lower()
        df['date'] = pd.to_datetime(df['date'])
        if start_date and end_date:
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        # Get the last management row per locality (includes observation)
        df_sorted = df.sort_values('date')
        last_dates = df_sorted.groupby('locality_id').tail(1).reset_index(drop=True)
        # Merge with locality info (name, latitude, longitude)
        localities = self.get_locality_data()
        localities = localities[['locality_id', 'name', 'LATITUDE', 'LONGITUDE']]
        localities = localities.rename(columns={'LATITUDE': 'latitude', 'LONGITUDE': 'longitude'})
        last_dates = last_dates.merge(localities, on='locality_id', how='left')
        today = pd.Timestamp.now().normalize()
        last_dates['days_since'] = (today - last_dates['date']).dt.days
        return last_dates[['locality_id', 'name', 'latitude', 'longitude', 'date', 'days_since', 'observation']]

    def get_days_since_last_monitoring(self, start_date=None, end_date=None):
        # Use get_dafor_data to get monitoring records
        df = self.get_dafor_data(start_date, end_date)
        # Ensure date is datetime
        df['date'] = pd.to_datetime(df['date'])
        # Get last monitoring date per locality
        last_dates = df.groupby('locality_id')['date'].max().reset_index()
        # Merge with locality info (name, latitude, longitude, coords_local)
        localities = self.get_locality_data()
        localities = localities[['locality_id', 'name', 'LATITUDE', 'LONGITUDE', 'coords_local']]
        localities = localities.rename(columns={'LATITUDE': 'latitude', 'LONGITUDE': 'longitude'})
        last_dates = last_dates.merge(localities, on='locality_id', how='left')
        today = pd.Timestamp.now().normalize()
        last_dates['days_since'] = (today - last_dates['date']).dt.days
        return last_dates

    def get_km_monitored(self, start_date=None, end_date=None):
        """Sum the lengths of all DAFOR lines (in kilometers) for the given date range."""
        df_dafor = self.get_dafor_data(start_date, end_date)
        df_dafor['length_m'] = df_dafor['dafor_coords'].apply(self.calculate_dafor_length)
        total_km = df_dafor['length_m'].sum() / 1000  # convert meters to kilometers
        return total_km

    def get_monitoring_events_by_locality(self, start_date=None, end_date=None):
        """
        Count the number of monitoring events (transects) per locality.
        Returns a DataFrame with locality_id, name, and event_count.
        """
        df_dafor = self.get_dafor_data(start_date, end_date)
        df_locality = self.get_locality_data()

        # Count events per locality
        event_counts = df_dafor.groupby('locality_id').size().reset_index(name='event_count')

        # Merge with locality data to get names and coordinates
        result = event_counts.merge(
            df_locality[['locality_id', 'name', 'LATITUDE', 'LONGITUDE']],
            on='locality_id',
            how='left'
        )

        return result

    def get_transect_coordinates_for_density(self, start_date=None, end_date=None):
        """
        Extract all transect coordinates for kernel density estimation.
        Interpolates points along line segments to create continuous coverage.
        Returns a DataFrame with individual coordinate points from all transects.
        """
        df_dafor = self.get_dafor_data(start_date, end_date)

        # Parse coordinates and interpolate along line segments
        points = []
        for _, row in df_dafor.iterrows():
            try:
                coords = json.loads(row['dafor_coords'])
                if coords and isinstance(coords, list) and len(coords) >= 2:
                    # Interpolate points along each line segment
                    for i in range(len(coords) - 1):
                        if isinstance(coords[i], list) and isinstance(coords[i+1], list):
                            start_lat, start_lon = coords[i]
                            end_lat, end_lon = coords[i+1]

                            # Calculate distance between points
                            try:
                                distance_m = geodesic((start_lat, start_lon), (end_lat, end_lon)).meters

                                # Create interpolated points every 5 meters along the segment
                                num_points = max(2, int(distance_m / 5))

                                for j in range(num_points):
                                    fraction = j / (num_points - 1) if num_points > 1 else 0
                                    interp_lat = start_lat + (end_lat - start_lat) * fraction
                                    interp_lon = start_lon + (end_lon - start_lon) * fraction

                                    points.append({
                                        'latitude': interp_lat,
                                        'longitude': interp_lon,
                                        'locality_id': row['locality_id'],
                                        'date': row['date']
                                    })
                            except Exception:
                                # If distance calculation fails, just use endpoints
                                points.append({
                                    'latitude': start_lat,
                                    'longitude': start_lon,
                                    'locality_id': row['locality_id'],
                                    'date': row['date']
                                })
                                points.append({
                                    'latitude': end_lat,
                                    'longitude': end_lon,
                                    'locality_id': row['locality_id'],
                                    'date': row['date']
                                })
            except Exception:
                continue

        return pd.DataFrame(points)
    def get_transect_lines_for_density(self, start_date=None, end_date=None):
        """
        Extract transect lines (not interpolated points) for line-based density visualization.
        Returns a list of transect line coordinates.
        """
        df_dafor = self.get_dafor_data(start_date, end_date)

        transect_lines = []
        for _, row in df_dafor.iterrows():
            try:
                coords = json.loads(row['dafor_coords'])
                if coords and isinstance(coords, list) and len(coords) >= 2:
                    transect_lines.append({
                        'coords': coords,
                        'locality_id': row['locality_id'],
                        'date': row['date']
                    })
            except Exception:
                continue

        return transect_lines
