from pymongo import MongoClient
import os

mongo_host = os.getenv('MONGO_HOST', 'mongo')
mongo_port = os.getenv('MONGO_PORT', '27017')
mongo_username = os.getenv('MONGO_USERNAME', 'root')
mongo_password = os.getenv('MONGO_PASSWORD', 'example')

client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/")
db = client['db']


def create_collection_with_validation(collection_name, schema):
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name, validator=schema)
        print(f"Collection {collection_name} created with validation")
    else:
        print(f"Collection {collection_name} already exists")


def initialize_schema():
    # categories
    categories_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["kategorie_nr", "bezeichnung"],
            "properties": {
                "kategorie_nr": {"bsonType": "int"},
                "ueber_kategorie": {"bsonType": ["int", "null"]},  # ref to other kategorie_nr
                "bezeichnung": {"bsonType": "string"},
                "color_code": {"bsonType": ["string", "null"]}
            }
        }
    }
    create_collection_with_validation("categories", categories_schema)

    # customer
    customers_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["kunde_nr", "firmen_kunde", "status_vip"],
            "properties": {
                "kunde_nr": {"bsonType": "int"},
                "firmen_kunde": {"bsonType": "bool"},
                "status_vip": {"bsonType": "bool"},
                "billing_address": {
                    "bsonType": ["object", "null"],
                    "properties": {
                        "land": {"bsonType": "string"},
                        "stadt": {"bsonType": "string"},
                        "strasse": {"bsonType": "string"},
                        "haus_nr": {"bsonType": "string"}
                    }
                },
                "customer_details": {
                    "bsonType": ["object", "null"],
                    "oneOf": [
                        {
                            "properties": {
                                "vorname": {"bsonType": "string"},
                                "nachname": {"bsonType": "string"}
                            },
                            "required": ["vorname", "nachname"]
                        },
                        {
                            "properties": {
                                "firmen_name": {"bsonType": "string"},
                                "steuer_nr": {"bsonType": ["string", "null"]}
                            },
                            "required": ["firmen_name"]
                        }
                    ]
                }
            }
        }
    }
    create_collection_with_validation("customers", customers_schema)

    # orders
    orders_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["bestell_nr", "datum", "delivery_address", "items"],
            "properties": {
                "bestell_nr": {"bsonType": "int"},
                "kunde_nr": {"bsonType": ["int", "null"]},
                "datum": {"bsonType": "date"},
                "delivery_address": {
                    "bsonType": "object",
                    "required": ["land", "stadt", "strasse", "haus_nr"],
                    "properties": {
                        "land": {"bsonType": "string"},
                        "stadt": {"bsonType": "string"},
                        "strasse": {"bsonType": "string"},
                        "haus_nr": {"bsonType": "string"}
                    }
                },
                "items": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["bestellung_artikel_nr", "artikel_nr"],
                        "properties": {
                            "bestellung_artikel_nr": {"bsonType": "int"},
                            "artikel_nr": {"bsonType": "int"}
                        }
                    }
                }
            }
        }
    }
    create_collection_with_validation("orders", orders_schema)

    # products
    products_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["artikel_nr", "bezeichnung", "preis_cent"],
            "properties": {
                "artikel_nr": {"bsonType": "int"},
                "kategorie_nr": {"bsonType": ["int", "null"]},
                "bezeichnung": {"bsonType": "string"},
                "preis_cent": {"bsonType": "int"},
                "inventory": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["raum_nr", "lager_nr"],
                        "properties": {
                            "raum_nr": {"bsonType": "int"},
                            "lager_nr": {"bsonType": "int"},
                            "anzahl": {"bsonType": ["int", "null"]}
                        }
                    }
                }
            }
        }
    }
    create_collection_with_validation("products", products_schema)

    # warehouse
    warehouses_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["lager_nr", "raum_anzahl"],
            "properties": {
                "lager_nr": {"bsonType": "int"},
                "raum_anzahl": {"bsonType": "int"},
                "address": {
                    "bsonType": ["object", "null"],
                    "properties": {
                        "land": {"bsonType": "string"},
                        "stadt": {"bsonType": "string"},
                        "strasse": {"bsonType": "string"},
                        "haus_nr": {"bsonType": "string"}
                    }
                },
                "rooms": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "required": ["raum_nr", "etage", "groesse"],
                        "properties": {
                            "raum_nr": {"bsonType": "int"},
                            "etage": {"bsonType": "int"},
                            "groesse": {"bsonType": "int"}
                        }
                    }
                }
            }
        }
    }
    create_collection_with_validation("warehouses", warehouses_schema)

    print("MongoDB schema initialized")


initialize_schema()
