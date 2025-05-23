from data.database import db_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    try:
        with db_manager.engine.connect() as conn:
            # Test basic query
            db_name = conn.execute("SELECT DATABASE()").fetchone()[0]
            logger.info(f"Connected to database: {db_name}")
            
            # Test table access
            tables = conn.execute("SHOW TABLES").fetchall()
            logger.info(f"Found {len(tables)} tables in database")
            
            return True
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False

if __name__ == "__main__":
    if test_connection():
        print("✓ Database connection successful!")
    else:
        print("✗ Database connection failed")