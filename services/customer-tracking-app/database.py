from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv(".env")
host = os.getenv("MONGO_HOST", "localhost")
client = MongoClient(f"mongodb://admin:admin@{host}:27017")

