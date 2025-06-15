import mysql.connector
import os

# use env instead of hardcoding
db_config = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "user"),
    "password": os.getenv("MYSQL_PASSWORD", "password"),
    "database": os.getenv("MYSQL_DATABASE", "db")
}

# path_sql = "../../sql/"
path_sql = "/app/sql"
# path_sql = "./docker-entrypoint-initdb.d/sql"


def get_connection():
    return mysql.connector.connect(**db_config)
