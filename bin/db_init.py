from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.get_database("keywords")
kw_db = db.get_collection("keywords")
