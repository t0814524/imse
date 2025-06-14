from db_config import get_connection
from flask import Flask, render_template, jsonify, request, session
from mysql.connector import Error


def register_customer(data):
    try:
        print(data)
        # Open a connection to the database
        connection = get_connection()
        cursor = connection.cursor()

        # Insert address into the adresse table (for the billing address)
        cursor.execute("""
            INSERT INTO adresse (land, stadt, strasse, haus_nr)
            VALUES (%s, %s, %s, %s)
        """, (data['land'], data['stadt'], data['strasse'], data['haus_nr']))
        connection.commit()

        # Get the address ID
        adresse_id = cursor.lastrowid

        # Insert customer into the kunde table
        cursor.execute("""
            INSERT INTO kunde (rechnungs_adresse_id, firmen_kunde, status_vip)
            VALUES (%s, %s, %s)
        """, (adresse_id, False, False))
        connection.commit()

        # Get the customer ID
        kunde_id = cursor.lastrowid

        # Insert private customer details into privatkunde table
        cursor.execute("""
            INSERT INTO privatkunde (kunde_nr, vorname, nachname)
            VALUES (%s, %s, %s)
        """, (kunde_id, data['vorname'], data['nachname']))
        connection.commit()

        # Store user information in the session
        session['user_id'] = kunde_id
        session['rechnungs_adresse_id'] = adresse_id

        return jsonify({"message": "Customer registered successfully!"}), 201
    except Error as err:
        connection.rollback()
        print(err)
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        connection.close()
