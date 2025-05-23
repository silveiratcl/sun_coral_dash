import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def test_mysql_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT', 3306)),
            ssl=None  # Or configure SSL parameters if needed
        )
        
        print("✓ Connection successful!")
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"MySQL Server version: {version[0]}")
            
    except pymysql.Error as e:
        print(f"✗ Connection failed: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    test_mysql_connection()