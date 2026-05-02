import mysql.connector
import os

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "UDAYsql123"),
        database=os.environ.get("DB_NAME", "task_manager"),
        port=os.environ.get("DB_PORT", 3306)
    )