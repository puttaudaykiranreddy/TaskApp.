import mysql.connector
import os

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST", "localhost"),
        user=os.environ.get("MYSQLUSER", "root"),
        password=os.environ.get("MYSQLPASSWORD", "UDAYsql123"),
        database=os.environ.get("MYSQLDATABASE", "task_manager"),
        port=int(os.environ.get("MYSQLPORT", 3306))
    )