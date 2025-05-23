import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
from functools import lru_cache
import logging
import pymysql

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.engine = self._create_engine()
        
    def _create_engine(self):
        """Create and return a SQLAlchemy engine"""
        try:
            DB_CONFIG = {
                'host': os.getenv('DB_HOST').strip(),
                'port': int(os.getenv('DB_PORT', 3306)),
                'database': os.getenv('DB_NAME').strip(),
                'user': os.getenv('DB_USER').strip(),
                'password': os.getenv('DB_PASS').strip()
            }
            
            # Verify all required variables are present
            if not all(DB_CONFIG.values()):
                missing = [k for k,v in DB_CONFIG.items() if not v]
                raise ValueError(f"Missing database configuration for: {missing}")
            
            logger.info(f"Connecting to {DB_CONFIG['database']} on {DB_CONFIG['host']}")
            
            connection_string = (
                f"mysql+pymysql://{DB_CONFIG['user']}:"
                f"{DB_CONFIG['password']}@"
                f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/"
                f"{DB_CONFIG['database']}"
                "?charset=utf8mb4"
            )
            
            engine = create_engine(
                connection_string,
                pool_size=5,
                pool_recycle=3600,
                pool_pre_ping=True
            )
            
            # Test connection
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            
            logger.info("Database connection established successfully")
            return engine
            
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            raise

# Initialize the database manager
db_manager = DatabaseManager()

@lru_cache(maxsize=32)
def get_management_data():
    """Get management data with caching"""
    query = """
    SELECT management_id, management_coords, observer, managed_mass_kg, date 
    FROM data_coralsol_management
    """
    with db_manager.engine.begin() as connection:
        df = pd.read_sql(query, con=connection)
    df.columns = map(str.lower, df.columns)
    return df

@lru_cache(maxsize=32)
def get_locality_data():
    """Get locality data with caching"""
    query = """
    SELECT locality_id, coords_local, name, date 
    FROM data_coralsol_locality
    """
    with db_manager.engine.begin() as connection:
        df = pd.read_sql(query, con=connection)
    df.columns = map(str.lower, df.columns)
    return df

@lru_cache(maxsize=32)
def get_occ_data():
    """Get occurrence data with caching"""
    query = """
    SELECT occurrence_id, spot_coords, date, depth, superficie_photo 
    FROM data_coralsol_occurrence 
    WHERE superficie_photo IS NOT NULL
    """
    with db_manager.engine.begin() as connection:
        df = pd.read_sql(query, con=connection)
    df.columns = map(str.lower, df.columns)
    return df

@lru_cache(maxsize=32)
def get_dafor_data():
    """Get DAFOR data with caching"""
    query = """
    SELECT dafor_id, locality_id, dafor_coords, date, 
           horizontal_visibility, bathymetric_zone, method, dafor_value 
    FROM data_coralsol_dafor
    """
    with db_manager.engine.begin() as connection:
        df = pd.read_sql(query, con=connection)
    df.columns = map(str.lower, df.columns)
    return df