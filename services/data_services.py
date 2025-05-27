import pandas as pd
import geopandas as gpd
from shapely import wkt
from functools import lru_cache
from config.database import db

class CoralDataService:
    @lru_cache(maxsize=1)
    def get_combined_data(self):
        """Combine data from all tables with proper geospatial handling"""
        localities = self._get_locality_data()
        occurrences = self._get_occurrence_data()
        management = self._get_management_data()
        
        # Merge data (example - adjust based on your relationships)
        df = pd.merge(
            occurrences,
            localities[['locality_id', 'geometry']],
            on='locality_id',
            how='left'
        )
        
        # Add management data
        df = pd.merge(
            df,
            management,
            on='locality_id',
            how='left'
        )
        
        # Convert to GeoDataFrame
        gdf = gpd.GeoDataFrame(df, geometry='geometry')
        return gdf

    def _get_locality_data(self):
        query = "SELECT locality_id, coords_local, name, date FROM data_coralsol_locality"
        df = self._execute_query(query)
        df['geometry'] = df['coords_local'].apply(wkt.loads)
        return gpd.GeoDataFrame(df, geometry='geometry')

    def _get_occurrence_data(self):
        query = """SELECT occurrence_id, locality_id, spot_coords, date, 
                   depth, superficie_photo FROM data_coralsol_occurrence"""
        df = self._execute_query(query)
        df['geometry'] = df['spot_coords'].apply(wkt.loads)
        return gpd.GeoDataFrame(df, geometry='geometry')

    def _get_management_data(self):
        query = """SELECT management_id, locality_id, management_coords, 
                   observer, managed_mass_kg, date FROM data_coralsol_management"""
        df = self._execute_query(query)
        df['geometry'] = df['management_coords'].apply(wkt.loads)
        return gpd.GeoDataFrame(df, geometry='geometry')

    def _execute_query(self, query):
        with db.get_session() as session:
            result = session.execute(text(query))
            return pd.DataFrame(result.fetchall(), columns=result.keys())