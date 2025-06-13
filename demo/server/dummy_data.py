import mysql.connector

from mysql.connector import Error


def create_or_replace_dummy_data():
    # connect db
    # conn = mysql.connector.connect(
    #     host="127.0.0.1",
    #     port=3306,
    #     user="user",
    #     password="password",
    #     database="db"
    # )

    # cursor = conn.cursor()

    # cursor.execute("SHOW TABLES;")

    # tables = cursor.fetchall()
    # print("Tables in the database:")
    # for table in tables:
    #     print(table)

    # cursor.close()
    # conn.close()

    # return "asdf"

    try:
        # Connecting to MySQL server in Docker
        conn = mysql.connector.connect(
            host='localhost',    # Use 'localhost' or '127.0.0.1'
            port=3306,           # Default MySQL port
            user='root',         # The MySQL user
            password='password',  # The root password you set in the Docker container
            database='db'        # The database you want to connect to
        )

        if conn.is_connected():
            print("Successfully connected to the database")

            # Creating a cursor object
            cursor = conn.cursor()

            # Example query
            cursor.execute("SHOW DATABASES;")
            print(cursor.fetchall())  # Fetch all the databases

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            conn.close()
            print("Connection closed.")
