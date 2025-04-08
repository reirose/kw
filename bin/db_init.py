import time
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

while True:
    try:
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)  # dev_link
        # client = MongoClient("mongodb://root:admin@mongodb:27017", serverSelectionTimeoutMS=5000)
        db = client.get_database("keywords")
        kw_db = db.get_collection("keywords")
        client.server_info()
        print("Connected to MongoDB")
        break
    except ServerSelectionTimeoutError:
        print("Waiting for MongoDB...")
        time.sleep(5)
