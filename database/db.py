import os
from pymongo import MongoClient

# TODO Enter this first in terminal (root directory) if not set yet:
# $env:MONGO_URI = "mongodb+srv://felipejrnoriel_db_user:aqwkTLilxErXraRO@fp-db.8nhcswv.mongodb.net/"
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("Please set MONGO_URI first. (from README.txt)")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

db = client["collected_data"]
collection = db["users"]
