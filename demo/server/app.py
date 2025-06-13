from flask import Flask, render_template
from dummy_data import create_or_replace_dummy_data

app = Flask(__name__)


@app.route("/dummy-data")
def dummy_data():
    print("dummy1")
    # Module Imports
    import mariadb
    import sys

    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user="root",
            password="password",
            host="mariadb",
            port=3306,
            database="db"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()
    return "succ"


@app.route("/dummy-data2")
def dummy_data2():
    print("creating dummy data")
    # res = create_or_replace_dummy_data()
    import mysql.connector

    mydb = mysql.connector.connect(
        host="mariadb1",
        port=3306,
        user="user",
        password="password",
        database="db"
    )

    print(mydb)

    return "created/replaced dummmy data"


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
