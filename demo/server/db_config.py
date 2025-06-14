import mysql.connector


db_config = {
    "host": "localhost",
    "port": 3333,
    "user": "user",
    "password": "password",
    "database": "db"
}


def get_connection():
    return mysql.connector.connect(**db_config)
