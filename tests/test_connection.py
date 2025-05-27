from config.database import db
from sqlalchemy import text

try:
    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        print("Connection successful! MySQL version:", result.scalar())
except Exception as e:
    print("Connection failed:", str(e))