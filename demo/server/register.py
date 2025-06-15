from db_config import get_connection
from flask import jsonify, session
from mysql.connector import Error


def register_customer(data):
    try:
        print(data)
        # connect to db
        connection = get_connection()
        cursor = connection.cursor()

        # adresse
        cursor.execute("""
            INSERT INTO adresse (land, stadt, strasse, haus_nr)
            VALUES (%s, %s, %s, %s)
        """, (data['land'], data['stadt'], data['strasse'], data['haus_nr']))
        connection.commit()

        adresse_id = cursor.lastrowid

        # kunde
        cursor.execute("""
            INSERT INTO kunde (rechnungs_adresse_id, firmen_kunde, status_vip)
            VALUES (%s, %s, %s)
        """, (adresse_id, data['firmen_kunde'], data['status_vip']))
        connection.commit()

        kunde_id = cursor.lastrowid

        # check if firmenkunde
        if data['firmen_kunde']:
            cursor.execute("""
                INSERT INTO firmenkunde (kunde_nr, firmen_name)
                VALUES (%s, %s)
            """, (kunde_id, data['business_name']))
            connection.commit()

        # privatkunde
        else:
            cursor.execute("""
                INSERT INTO privatkunde (kunde_nr, vorname, nachname)
                VALUES (%s, %s, %s)
            """, (kunde_id, data['vorname'], data['nachname']))
            connection.commit()

        # store session, for checkout
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
