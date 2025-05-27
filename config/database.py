import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import load_dotenv
import logging
import pymysql

from functools import lru_cache

# Configure logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Database:
    def __init__(self):
        load_dotenv()
        self._validate_env_vars()
        self.DB_URL = self._build_connection_string()
        self.engine = self._create_engine()
        self._verify_connection()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logger.info("Database connection initialized successfully")

    def _validate_env_vars(self):
        required_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_NAME']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

    def _build_connection_string(self):
        """Build properly encoded connection string"""
        username = quote_plus(os.getenv('DB_USER'))
        password = quote_plus(os.getenv('DB_PASSWORD'))
        host = os.getenv('DB_HOST')
        
        # Handle IPv6 addresses
        if os.getenv('DB_USE_IPV6', '').lower() == 'true' and ':' in host and not host.startswith('['):
            host = f"[{host}]"
            
        return (
            f"mysql+pymysql://{username}:{password}@"
            f"{host}:{os.getenv('DB_PORT', '3306')}/"
            f"{quote_plus(os.getenv('DB_NAME'))}"
            "?charset=utf8mb4"
            "&connect_timeout=10"
            "&ssl_disabled=true"
        )

    def _create_engine(self):
        """Create engine with proper MySQL/MariaDB configuration"""
        pymysql.install_as_MySQLdb()
        
        return create_engine(
            self.DB_URL,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=True,
            connect_args={
                'connect_timeout': 10,
                'local_infile': True
            }
        )

    def _verify_connection(self):
        """Enhanced connection verification"""
        try:
            with self.engine.connect() as conn:
                version = conn.execute(text("SELECT VERSION()")).scalar()
                logger.info(f"Connected to database version: {version}")
        except Exception as e:
            logger.error("Connection failed. Please verify:")
            logger.error(f"1. Host: {os.getenv('DB_HOST')}")
            logger.error(f"2. Username: {os.getenv('DB_USER')}")
            logger.error("3. Password: ***** (set correctly?)")
            logger.error("4. Database name: {os.getenv('DB_NAME')}")
            logger.error("5. Port: {os.getenv('DB_PORT', '3306')}")
            logger.error("6. Firewall rules (if applicable)")
            raise ConnectionError(f"Database connection failed: {str(e)}") from e

    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            session.close()

# Initialize database connection
try:
    db = Database()
except Exception as e:
    logger.critical(f"Failed to initialize database: {str(e)}")
    raise

class DataService:
    @lru_cache(maxsize=32)
    def get_data(self, query, params=None):
        with self.get_session() as session:
            result = session.execute(text(query), params or {})
            return result.fetchall()