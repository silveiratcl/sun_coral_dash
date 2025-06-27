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