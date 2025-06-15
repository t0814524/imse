from flask import Flask, render_template, jsonify, request, session, redirect
from dummy_data import create_or_replace_dummy_data
import mysql.connector
from mysql.connector import Error
from register import register_customer

from db_config import get_connection
from flask_session import Session
import uuid
from migrate import migrate

import mongo

app = Flask(__name__)
# Set secret key for session management
app.secret_key = str(uuid.uuid4())

# For storing the session in a file (optional, but useful for persistent sessions)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


def execute_sql_script(path):

    connection = get_connection()

    cursor = connection.cursor()

    # Read the SQL script from file
    with open(path, 'r') as file:
        script = file.read()

    try:
        # Split the script into individual statements (based on ';' delimiter)
        statements = script.split(';')

        # Execute each statement
        for statement in statements:
            statement = statement.strip()  # Remove any leading/trailing spaces
            if statement:  # Ignore empty statements
                cursor.execute(statement)

        connection.commit()  # Commit any changes made (if necessary)
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
        # Connect to the database
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Query the view
        cursor.execute("SELECT * FROM view_all_articles")
        articles = cursor.fetchall()

        # Return the articles as JSON
        return jsonify(articles)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/api/checkout', methods=['POST'])
def checkout_api():
    try:
        cart = request.get_json()
        print("cart")
        print(cart)

        # Ensure the cart is not empty
        if not cart or len(cart) == 0:
            return jsonify({"error": "Cart is empty!"}), 400

        # Simulate a logged-in user; in a real app, use session or token
        user_id = 1  # For demonstration, assuming the logged-in user's ID is 1

        # Connect to the database
        conn = get_connection()
        cursor = conn.cursor()

        # Step 1: Validate delivery address (liefer_adresse_id)
        liefer_adresse_id = cart[0].get('liefer_adresse_id')  # Assuming all items in cart share the same delivery address
        print("sofar works todo")

        if not liefer_adresse_id:
            return jsonify({"error": "Missing or invalid delivery address."}), 400

        # Step 2: Create a new order in the `bestellung` table
        cursor.execute("""
            INSERT INTO bestellung (kunde_nr, liefer_adresse_id)
            VALUES (%s, %s)
        """, (user_id, liefer_adresse_id))

        # Get the generated order number (bestell_nr)
        bestell_nr = cursor.lastrowid

        # Step 3: Insert items into the `bestellung_artikel` table
        for item in cart:
            artikel_id = item['artikel_id']
            quantity = item['quantity']
            price_in_cents = item['price_in_cents']

            # Inserting each article into the order
            cursor.execute("""
                INSERT INTO bestellung_artikel (bestell_nr, artikel_nr)
                VALUES (%s, %s)
            """, (bestell_nr, artikel_id))

            # Decrementing the stock for the article in the warehouse (artikel_raum)
            cursor.execute("""
                UPDATE artikel_raum
                SET anzahl = anzahl - %s
                WHERE artikel_nr = %s
            """, (quantity, artikel_id))

        # Commit the changes to the database
        conn.commit()

        # Return success response with the order ID
        return jsonify({"message": "Order placed successfully!", "order_id": bestell_nr}), 200

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({"error": str(err)}), 500

    except Exception as e:
        print(e)
        print(f"General error: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    print("session")
    print(session)
    user_id = session.get('user_id')
    rechnungs_adresse_id = session.get('rechnungs_adresse_id')

    if not user_id or not rechnungs_adresse_id:
        return redirect('/register')  # redirect to login page if no session data, for now to register page

    if request.method == 'POST':
        # If the user provides a different delivery address
        data = request.get_json()
        print("data")
        print(data)

        # If no delivery address is provided, use the billing address
        print("liefer_adresse_id")
        liefer_adresse_id = data.get('liefer_adresse_id', rechnungs_adresse_id)
        print(liefer_adresse_id)

        # Create an order in the database
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Step 1: Create a new order in the `bestellung` table
            cursor.execute("""
                INSERT INTO bestellung (kunde_nr, liefer_adresse_id)
                VALUES (%s, %s)
            """, (user_id, liefer_adresse_id))
            conn.commit()

            # Get the generated order number (bestell_nr)
            bestell_nr = cursor.lastrowid

            # Step 2: Insert items into the `bestellung_artikel` table
            cart = data.get('cart', [])
            for item in cart:
                artikel_id = item['artikel_id']
                quantity = item['quantity']
                cursor.execute("""
                    INSERT INTO bestellung_artikel (bestell_nr, artikel_nr)
                    VALUES (%s, %s)
                """, (bestell_nr, artikel_id))

                # Decrement stock in `artikel_raum`
                cursor.execute("""
                    UPDATE artikel_raum
                    SET anzahl = anzahl - %s
                    WHERE artikel_nr = %s
                """, (quantity, artikel_id))

            conn.commit()

            # Return success response with the order ID
            return jsonify({"message": "Order placed successfully!", "order_id": bestell_nr}), 200

        except Error as err:
            conn.rollback()
            return jsonify({"error": str(err)}), 500

        finally:
            cursor.close()
            conn.close()

    # GET method (render checkout page, passing customer info)
    return render_template('checkout.html', user_id=user_id, rechnungs_adresse_id=rechnungs_adresse_id)


@app.route('/api/get_billing_address', methods=['GET'])
def get_billing_address():
    try:
        # Retrieve the logged-in user's ID from session
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "User not logged in"}), 400

        # Connect to the database
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Query the billing address from the database
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
    print("creating dummy data")
    # res = create_or_replace_dummy_data()
    path_delete_data_sql = "../../sql/delete_data.sql"
    path_create_dummy_data_sql = "../../sql/create_dummy_data.sql"
    execute_sql_script(path_delete_data_sql)
    execute_sql_script(path_create_dummy_data_sql)

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
    file_path = "../../sql/report.sql"
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
            print(result)
            return jsonify(result)
        finally:
            # Close the connection
            cursor.close()
            conn.close()


# Route to get customer details
@app.route('/api/me', methods=['GET'])
def get_user_details():
    if 'kunde_nr' not in session:
        return jsonify({"error": "User not logged in"}), 401

    # Retrieve customer details from the database
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM privatkunde WHERE kunde_nr = %s", (session['kunde_nr'],))
    user = cursor.fetchone()

    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


# Route for registration page (the form)
@app.route('/register')
def register_page():
    return render_template("register.html")  # This is the registration form.

# API route for registering a customer


@app.route('/api/register', methods=['POST'])
def _register_customer():
    data = request.get_json()
    return register_customer(data)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
