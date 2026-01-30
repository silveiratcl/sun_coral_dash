import pandas as pd
import json
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
        query = "SELECT management_id, Locality_id, Management_coords, Date, Observer, Depth, Number_of_divers, Method, Managed_mass_kg, Observation, occurrences_managed FROM data_coralsol_management"
        df = pd.read_sql(query, db.engine)
        df.columns = df.columns.str.lower()

        df['date'] = pd.to_datetime(df['date'], dayfirst=True)

        if start_date and end_date:
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        return df[['management_id', 'locality_id', 'management_coords', 'date', 'observer', 'depth', 'number_of_divers', 'method', 'managed_mass_kg', 'observation', 'occurrences_managed']]

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
