import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def test_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT', '3306')),
            connect_timeout=10,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                result = cursor.fetchone()
                print("✓ MySQL Server Version:", result)
                
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print(f"✓ Found {len(tables)} tables in database")
                
        return True
        
    except pymysql.Error as e:
        print(f"✗ MySQL Error {e.args[0]}: {e.args[1]}")
        return False
    except Exception as e:
        print(f"✗ General Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()