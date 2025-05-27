from sqlalchemy import text
from config.database import db
import pandas as pd
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

class CoralDataRepository:
    @staticmethod
    def _execute_query(query, params=None):
        try:
            with db.get_session() as session:
                result = session.execute(text(query), params or {})
                return result.fetchall()
        except Exception as e:
            logger.error(f"Query failed: {str(e)}")
            raise

    @staticmethod
    def _to_dataframe(results, columns=None):
        if not results:
            return pd.DataFrame()
            
        if columns:
            return pd.DataFrame(results, columns=columns)
        return pd.DataFrame(results)

    @staticmethod
    @lru_cache(maxsize=32)
    def get_management_data():
        query = """
        SELECT management_id, management_coords, observer, 
               managed_mass_kg, date 
        FROM data_coralsol_management
        """
        results = CoralDataRepository._execute_query(query)
        df = CoralDataRepository._to_dataframe(results)
        df.columns = map(str.lower, df.columns)
        return df

    @staticmethod
    @lru_cache(maxsize=32)
    def get_locality_data():
        query = """
        SELECT locality_id, coords_local, name, date 
        FROM data_coralsol_locality
        """
        results = CoralDataRepository._execute_query(query)
        df = CoralDataRepository._to_dataframe(results)
        df.columns = map(str.lower, df.columns)
        return df

    @staticmethod
    @lru_cache(maxsize=32)
    def get_occ_data(limit=10):
        query = """
        SELECT Occurrence_id, Spot_coords, Date, Depth, Superficie_photo 
        FROM data_coralsol_occurrence 
        WHERE Superficie_photo IS NOT NULL
        LIMIT :limit
        """
        results = CoralDataRepository._execute_query(query, {'limit': limit})
        df = CoralDataRepository._to_dataframe(results)
        df.columns = map(str.lower, df.columns)
        return df

    @staticmethod
    @lru_cache(maxsize=32)
    def get_dafor_data():
        query = """
        SELECT Dafor_id, Locality_id, Dafor_coords, Date, 
               Horizontal_visibility, Bathymetric_zone, Method, Dafor_value 
        FROM data_coralsol_dafor
        """
        results = CoralDataRepository._execute_query(query)
        df = CoralDataRepository._to_dataframe(results)
        df.columns = map(str.lower, df.columns)
        return df