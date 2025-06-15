from pymongo import MongoClient
from bson import ObjectId
import os
# todo
# Connect to MongoDB

mongo_host = os.getenv('MONGO_HOST', 'mongo')
mongo_port = os.getenv('MONGO_PORT', '27017')
mongo_username = os.getenv('MONGO_USERNAME', 'root')
mongo_password = os.getenv('MONGO_PASSWORD', 'example')

# Connect to MongoDB
client = MongoClient(f"mongodb://{mongo_username}:{mongo_password}@{mongo_host}:{mongo_port}/")

db = client['db']  # Switch to the 'db' database (will create if not exists)


def create_collection_with_validation(collection_name, schema):
    # Check if the collection already exists
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name, validator=schema)
        print(f"Collection {collection_name} created with validation")
    else:
        print(f"Collection {collection_name} already exists")


# Create Address Schema
adresse_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["land", "stadt", "strasse", "haus_nr"],
        "properties": {
            "land": {"bsonType": "string", "description": "must be a string"},
            "stadt": {"bsonType": "string", "description": "must be a string"},
            "strasse": {"bsonType": "string", "description": "must be a string"},
            "haus_nr": {"bsonType": "string", "description": "must be a string"},
        }
    }
}
create_collection_with_validation("adresse", adresse_schema)

# Create other collections similarly (kunde, bestellung, etc.)
