from pymongo import MongoClient
from pymongo.collection import Collection
import os
try:
    from dotenv import load_dotenv
    load_dotenv('./.env')
except ModuleNotFoundError:
    pass

CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017/")

client = MongoClient(CONNECTION_STRING)
db = client["tracking_db"]  # Create or select the database


# Dependency function for getting the database collection
def get_db() -> Collection:
    return db
