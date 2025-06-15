'''
todo simone:
das is mal chatgpt (ka wie gut. hat noch errors, kann schon auf der main page getriggert werden) genauso wie mongo.py groesstenteils. 
hier muessten sinnvolle collections erstellt werden basierend auf create.sql (am besten zuerst mal was fur den usecase verwendet wird)
und dann von sql ausgelesen und in mongo geschrieben. 
sollt eig recht machbar sein fur heute noch und bring relativ viele punkte
'''
import mysql.connector
from pymongo import MongoClient
from bson import ObjectId
from db_config import get_connection as get_connection_sql

# MySQL connection settings
mysql_config = {
    'host': 'localhost',
    'user': 'user',
    'password': 'password',
    'database': 'db'
}


def migrate():

    # MongoDB connection settings
    mongo_uri = "mongodb://root:example@localhost:27018/"
    client = MongoClient(mongo_uri)
    db = client['db']

    # MySQL connection
    mysql_conn = get_connection_sql()
    cursor = mysql_conn.cursor(dictionary=True)

    # 1. Helper function to insert data into MongoDB

    def insert_data(collection_name, data):
        collection = db[collection_name]
        result = collection.insert_many(data)
        return result.inserted_ids

    # 2. Migrate Data from SQL to MongoDB

    # Migrate adresse
    cursor.execute("SELECT * FROM adresse")
    adresse_data = cursor.fetchall()
    adresse_ids = insert_data('adresse', adresse_data)

    # Migrate kunde
    cursor.execute("SELECT * FROM kunde")
    kunde_data = cursor.fetchall()
    for kunde in kunde_data:
        # Link rechnungs_adresse_id with MongoDB ObjectId
        adresse_id = adresse_ids[kunde['rechnungs_adresse_id'] - 1]  # Adjust for 0-indexed list
        kunde['rechnungs_adresse_id'] = adresse_id
    insert_data('kunde', kunde_data)

    # Migrate bestellung
    cursor.execute("SELECT * FROM bestellung")
    bestellung_data = cursor.fetchall()
    for bestellung in bestellung_data:
        # Link kunde_nr and liefer_adresse_id with MongoDB ObjectId
        kunde_id = bestellung['kunde_nr']  # Customer ID
        liefer_adresse_id = adresse_ids[bestellung['liefer_adresse_id'] - 1]  # Delivery address
        bestellung['kunde_nr'] = kunde_id
        bestellung['liefer_adresse_id'] = liefer_adresse_id
    insert_data('bestellung', bestellung_data)

    # Migrate lager
    cursor.execute("SELECT * FROM lager")
    lager_data = cursor.fetchall()
    for lager in lager_data:
        # Link lager_adresse_id with MongoDB ObjectId
        lager_adresse_id = adresse_ids[lager['lager_adresse_id'] - 1]  # Warehouse address
        lager['lager_adresse_id'] = lager_adresse_id
    insert_data('lager', lager_data)

    # Migrate raum
    cursor.execute("SELECT * FROM raum")
    raum_data = cursor.fetchall()
    insert_data('raum', raum_data)

    # Migrate kategorie
    cursor.execute("SELECT * FROM kategorie")
    kategorie_data = cursor.fetchall()
    insert_data('kategorie', kategorie_data)

    # Migrate artikel
    cursor.execute("SELECT * FROM artikel")
    artikel_data = cursor.fetchall()
    for artikel in artikel_data:
        # Link kategorie_nr with MongoDB ObjectId
        kategorie_id = artikel['kategorie_nr']  # Category ID
        artikel['kategorie_nr'] = kategorie_id
    insert_data('artikel', artikel_data)

    # Migrate artikel_raum
    cursor.execute("SELECT * FROM artikel_raum")
    artikel_raum_data = cursor.fetchall()
    insert_data('artikel_raum', artikel_raum_data)

    # Migrate bestellung_artikel
    cursor.execute("SELECT * FROM bestellung_artikel")
    bestellung_artikel_data = cursor.fetchall()
    insert_data('bestellung_artikel', bestellung_artikel_data)

    # Close the SQL connection
    cursor.close()
    mysql_conn.close()

    print("Data migration from SQL to MongoDB completed.")
