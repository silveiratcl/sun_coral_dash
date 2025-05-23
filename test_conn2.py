import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def test_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST').strip(),
            user=os.getenv('DB_USER').strip(),
            password=os.getenv('DB_PASS').strip(),
            database=os.getenv('DB_NAME').strip(),
            port=int(os.getenv('DB_PORT', 3306)),
            connect_timeout=10
        )
        
        print("✓ Connection successful!")
        
        with connection.cursor() as cursor:
            # Test basic query
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()
            print(f"Connected to database: {db_name[0]}")
            
            # List available tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"Available tables: {[t[0] for t in tables]}")
            
    except pymysql.Error as e:
        print(f"✗ Connection failed: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == "__main__":
    test_connection()