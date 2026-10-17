import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
print(
  "-> DEBUG in db.py: MONGO_URI is:", repr(MONGO_URI)
)

if not MONGO_URI:
  raise ValueError("Please set MONGO_URI first. (from README.txt)")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

db = client["collected_data"]
collection = db["users"]