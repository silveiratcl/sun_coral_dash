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


