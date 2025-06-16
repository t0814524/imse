import mysql.connector
from pymongo import MongoClient
import os


def migrate():

    mysql_conn = None
    mongo_client = None

    try:
        mysql_conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'mariadb'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            user=os.getenv('MYSQL_USER', 'user'),
            password=os.getenv('MYSQL_PASSWORD', 'password'),
            database=os.getenv('MYSQL_DATABASE', 'db')
        )

        mongo_host = os.getenv('MONGO_HOST', 'mongo')
        mongo_port = os.getenv('MONGO_PORT', '27017')
        mongo_username = os.getenv('MONGO_USERNAME', 'root')
        mongo_password = os.getenv('MONGO_PASSWORD', 'example')

        mongo_client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/")
        mongo_db = mongo_client.db

        print("Database connections established")

        # clear
        clear_collections(mongo_db)

        migrate_categories(mysql_conn, mongo_db)
        migrate_customers(mysql_conn, mongo_db)
        migrate_products(mysql_conn, mongo_db)
        migrate_warehouses(mysql_conn, mongo_db)
        migrate_orders(mysql_conn, mongo_db)

        print("Migration completed successfully")

    except Exception as e:
        print(f"Migration failed: {str(e)}")
        raise e

    finally:
        if mysql_conn:
            mysql_conn.close()
        if mongo_client:
            mongo_client.close()


def clear_collections(mongo_db):
    collections = ['categories', 'customers', 'orders', 'products', 'warehouses']
    for collection in collections:
        mongo_db[collection].delete_many({})
    print("MongoDB collections cleared")


def migrate_categories(mysql_conn, mongo_db):
    cursor = mysql_conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kategorie")
    categories = cursor.fetchall()

    if categories:
        mongo_db.categories.insert_many(categories)
        print(f"Migrated {len(categories)} categories")

    cursor.close()


def migrate_customers(mysql_conn, mongo_db):
    cursor = mysql_conn.cursor(dictionary=True)

    # get customers with address
    query = """
    SELECT k.kunde_nr, k.rechnungs_adresse_id, k.firmen_kunde, k.status_vip,
           a.land, a.stadt, a.strasse, a.haus_nr,
           p.vorname, p.nachname,
           f.firmen_name, f.steuer_nr
    FROM kunde k
    LEFT JOIN adresse a ON k.rechnungs_adresse_id = a.adresse_id
    LEFT JOIN privatkunde p ON k.kunde_nr = p.kunde_nr
    LEFT JOIN firmenkunde f ON k.kunde_nr = f.kunde_nr
    """

    cursor.execute(query)
    customers = cursor.fetchall()

    documents = []
    for customer in customers:
        doc = {
            "kunde_nr": customer['kunde_nr'],
            "firmen_kunde": bool(customer['firmen_kunde']),
            "status_vip": bool(customer['status_vip'])
        }

        # rechnungsaddr
        if customer['land']:
            doc["billing_address"] = {
                "land": customer['land'],
                "stadt": customer['stadt'],
                "strasse": customer['strasse'],
                "haus_nr": customer['haus_nr']
            }

        # firmen / privat
        if customer['firmen_kunde']:
            if customer['firmen_name']:
                doc["customer_details"] = {
                    "firmen_name": customer['firmen_name'],
                    "steuer_nr": customer['steuer_nr']
                }
        else:
            if customer['vorname'] and customer['nachname']:
                doc["customer_details"] = {
                    "vorname": customer['vorname'],
                    "nachname": customer['nachname']
                }

        documents.append(doc)

    if documents:
        mongo_db.customers.insert_many(documents)
        print(f"Migrated {len(documents)} customers")

    cursor.close()


def migrate_products(mysql_conn, mongo_db):
    cursor = mysql_conn.cursor(dictionary=True)

    query = """
    SELECT a.artikel_nr, a.kategorie_nr, a.bezeichnung, a.preis_cent,
           ar.raum_nr, ar.lager_nr, ar.anzahl
    FROM artikel a
    LEFT JOIN artikel_raum ar ON a.artikel_nr = ar.artikel_nr
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    products_dict = {}
    for row in rows:
        artikel_nr = row['artikel_nr']

        if artikel_nr not in products_dict:
            products_dict[artikel_nr] = {
                "artikel_nr": artikel_nr,
                "kategorie_nr": row['kategorie_nr'],
                "bezeichnung": row['bezeichnung'],
                "preis_cent": row['preis_cent'],
                "inventory": []
            }

        if row['raum_nr'] and row['lager_nr']:
            inventory_item = {
                "raum_nr": row['raum_nr'],
                "lager_nr": row['lager_nr'],
                "anzahl": row['anzahl']
            }
            products_dict[artikel_nr]["inventory"].append(inventory_item)

    documents = list(products_dict.values())
    if documents:
        mongo_db.products.insert_many(documents)
        print(f"Migrated {len(documents)} products")

    cursor.close()


def migrate_warehouses(mysql_conn, mongo_db):
    cursor = mysql_conn.cursor(dictionary=True)

    query = """
    SELECT l.lager_nr, l.raum_anzahl,
           a.land, a.stadt, a.strasse, a.haus_nr,
           r.raum_nr, r.etage, r.groesse
    FROM lager l
    LEFT JOIN adresse a ON l.lager_adresse_id = a.adresse_id
    LEFT JOIN raum r ON l.lager_nr = r.lager_nr
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    warehouses_dict = {}
    for row in rows:
        lager_nr = row['lager_nr']

        if lager_nr not in warehouses_dict:
            warehouses_dict[lager_nr] = {
                "lager_nr": lager_nr,
                "raum_anzahl": row['raum_anzahl'],
                "rooms": []
            }

            if row['land']:
                warehouses_dict[lager_nr]["address"] = {
                    "land": row['land'],
                    "stadt": row['stadt'],
                    "strasse": row['strasse'],
                    "haus_nr": row['haus_nr']
                }

        if row['raum_nr']:
            room = {
                "raum_nr": row['raum_nr'],
                "etage": row['etage'],
                "groesse": row['groesse']
            }
            warehouses_dict[lager_nr]["rooms"].append(room)

    documents = list(warehouses_dict.values())
    if documents:
        mongo_db.warehouses.insert_many(documents)
        print(f"Migrated {len(documents)} warehouses")

    cursor.close()


def migrate_orders(mysql_conn, mongo_db):
    cursor = mysql_conn.cursor(dictionary=True)

    # bestellung_artikel_nr not rlly necessary todl
    query = """
    SELECT b.bestell_nr, b.kunde_nr, b.datum,
           da.land as delivery_land, da.stadt as delivery_stadt,
           da.strasse as delivery_strasse, da.haus_nr as delivery_haus_nr,
           ba.bestellung_artikel_nr, ba.artikel_nr 
    FROM bestellung b
    LEFT JOIN adresse da ON b.liefer_adresse_id = da.adresse_id
    LEFT JOIN bestellung_artikel ba ON b.bestell_nr = ba.bestell_nr
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    orders_dict = {}
    for row in rows:
        bestell_nr = row['bestell_nr']

        if bestell_nr not in orders_dict:
            orders_dict[bestell_nr] = {
                "bestell_nr": bestell_nr,
                "kunde_nr": row['kunde_nr'],
                "datum": row['datum'],
                "delivery_address": {
                    "land": row['delivery_land'] or "",
                    "stadt": row['delivery_stadt'] or "",
                    "strasse": row['delivery_strasse'] or "",
                    "haus_nr": row['delivery_haus_nr'] or ""
                },
                "items": []
            }

        if row['bestellung_artikel_nr']:
            item = {
                "bestellung_artikel_nr": row['bestellung_artikel_nr'],
                "artikel_nr": row['artikel_nr']
            }
            orders_dict[bestell_nr]["items"].append(item)

    documents = list(orders_dict.values())
    if documents:
        mongo_db.orders.insert_many(documents)
        print(f"Migrated {len(documents)} orders")

    cursor.close()
