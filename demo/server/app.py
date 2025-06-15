from flask import Flask, render_template, jsonify, request, session, redirect
import mysql.connector
from mysql.connector import Error
from register import register_customer

from db_config import get_connection, path_sql
from flask_session import Session
import uuid
# from migrate import migrate todo

import mongo

app = Flask(__name__)

# secret for session
app.secret_key = str(uuid.uuid4())

# for persistence
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


def execute_sql_script(path):

    connection = get_connection()
    cursor = connection.cursor()

    with open(path, 'r') as file:
        script = file.read()

    try:
        statements = script.split(';')

        for statement in statements:
            statement = statement.strip()
            if statement:
                cursor.execute(statement)

        connection.commit()
        print("SQL script executed successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        connection.close()


@app.route('/articles', methods=['GET'])
def articles():
    return render_template("articles.html")


@app.route('/api/articles', methods=['GET'])
def get_articles():
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM view_all_articles")  # created this view in create.sql
        articles = cursor.fetchall()

        return jsonify(articles)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # print("session")
    # print(session)
    user_id = session.get('user_id')
    rechnungs_adresse_id = session.get('rechnungs_adresse_id')
    # clear session on dummy data creation to avoid bug here
    # try:
    #     addr = get_billing_address()  # check here if the addr can be fetched otherwise user likely is not logged in or the db got cleared
    #     print(addr.json())
    # except Exception as e:
    #     print(e)
    #     return redirect('/register')  # redirect to login page if no session data, for now to register page

    if not user_id or not rechnungs_adresse_id:
        return redirect('/register')  # redirect to login page if no session data, for now to register page

    if request.method == 'POST':
        # todo allow diffrent address
        data = request.get_json()

        liefer_adresse_id = data.get('liefer_adresse_id', rechnungs_adresse_id)  # rn dont send liefer addr so it defaults to rechnung_adresse_id
        print(liefer_adresse_id)

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # bestellung
            cursor.execute("""
                INSERT INTO bestellung (kunde_nr, liefer_adresse_id)
                VALUES (%s, %s)
            """, (user_id, liefer_adresse_id))
            conn.commit()

            bestell_nr = cursor.lastrowid

            # bestellung_artikel
            cart = data.get('cart', [])
            for item in cart:
                artikel_id = item['artikel_id']
                quantity = item['quantity']

                for _ in range(quantity):  # add multiple entries if quantity is > 1
                    cursor.execute("""
                        INSERT INTO bestellung_artikel (bestell_nr, artikel_nr)
                        VALUES (%s, %s)
                    """, (bestell_nr, artikel_id))

                # decrement stock in `artikel_raum`
                cursor.execute("""
                    UPDATE artikel_raum
                    SET anzahl = anzahl - %s
                    WHERE artikel_nr = %s
                """, (quantity, artikel_id))

            conn.commit()

            return jsonify({"message": "Order placed successfully!", "order_id": bestell_nr}), 200

        except Error as err:
            conn.rollback()
            return jsonify({"error": str(err)}), 500

        finally:
            cursor.close()
            conn.close()

    # GET method (render checkout page, passing customer info)
    # return render_template('checkout.html', user_id=user_id, rechnungs_adresse_id=rechnungs_adresse_id) todo
    return render_template('checkout.html')


@app.route('/api/get_billing_address', methods=['GET'])
def get_billing_address():
    try:
        # get user_id
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "User not logged in"}), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # get address details
        cursor.execute("""
            SELECT land, stadt, strasse, haus_nr
            FROM adresse
            WHERE adresse_id = (SELECT rechnungs_adresse_id FROM kunde WHERE kunde_nr = %s)
        """, (user_id,))
        address = cursor.fetchone()

        if not address:
            return jsonify({"error": "Billing address not found"}), 404
        return jsonify(address)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/dummy-data")
def dummy_data():
    path_delete_data_sql = path_sql + "/delete_data.sql"
    path_create_dummy_data_sql = path_sql + "/create_dummy_data.sql"
# todo:
    # try:
    #     conn = get_connection()
    #     cursor = conn.cursor(dictionary=True)

    #     # get address details
    #     cursor.execute("""
    #         SELECT land, stadt, strasse, haus_nr
    #         FROM adresse
    #         WHERE adresse_id = (SELECT rechnungs_adresse_id FROM kunde WHERE kunde_nr = %s)
    #     """, (user_id,))
    #     address = cursor.fetchone()

    #     if not address:
    #         return jsonify({"error": "Billing address not found"}), 404
    #     return jsonify(address)

    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500
    # finally:
    #     cursor.close()
    #     conn.close()
    execute_sql_script(path_delete_data_sql)
    execute_sql_script(path_create_dummy_data_sql)
    session.clear()

    # print(mydb)
    # execute_sql_script("../../sql/create_dummy_data.sql")  # todo: other path inside container

    return "created/replaced dummmy data"


@app.route("/migrate")
def _migrate():
    print("migrate data")
    migrate()
    return "created/replaced dummmy data"


@app.route('/report', methods=['GET'])
def get_report():
    file_path = path_sql + "/report.sql"
    with open(file_path, 'r') as file:
        query = file.read()

        # this line somehow is an issue in the query if i read it from report.sql:
        # SET @filter_date = '2025-04-01';

        query_lines = query.splitlines()
        query_without_set = "\n".join(query_lines[1:])  # remove first line (set filter)

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            filter_date = '2025-04-01'

            # set filter date in seperate query otherwise it did not work when reading form file
            cursor.execute(f"SET @filter_date = '{filter_date}';")

            # print(query_without_set)
            cursor.execute(query_without_set)
            result = cursor.fetchall()
            # print(result)
            return jsonify(result)
        finally:
            cursor.close()
            conn.close()


@app.route('/register')
def register_page():
    return render_template("register.html")


@app.route('/api/register', methods=['POST'])
def _register_customer():
    data = request.get_json()
    return register_customer(data)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5555, host="0.0.0.0", debug=True)  # host is important for docker to be accessable!!!
