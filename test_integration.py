from data.database import (
    db_manager,
    get_management_data,
    get_locality_data,
    get_occ_data,
    get_dafor_data
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_all_components():
    # Test raw connection
    try:
        with db_manager.engine.connect() as conn:
            result = conn.execute("SELECT DATABASE()").fetchone()
            logger.info(f"Connected to database: {result[0]}")
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False
    
    # Test each query function
    tests = [
        ("Management Data", get_management_data),
        ("Locality Data", get_locality_data),
        ("Occurrence Data", get_occ_data),
        ("DAFOR Data", get_dafor_data)
    ]
    
    for name, query_func in tests:
        try:
            df = query_func()
            logger.info(f"{name} loaded successfully - {len(df)} rows")
            print(df.head(2))
        except Exception as e:
            logger.error(f"Failed to load {name}: {e}")
            return False
    
    return True

if __name__ == "__main__":
    if test_all_components():
        print("✓ All components working correctly!")
    else:
        print("✗ Some tests failed")