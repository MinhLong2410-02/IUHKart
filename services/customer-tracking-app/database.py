from pymongo import MongoClient
from dotenv import load_dotenv
import os, redis
import psycopg2
load_dotenv(".env")
host = os.getenv("MONGO_HOST", "localhost")
mongo_client = MongoClient(f"mongodb://admin:admin@{host}:27017")
track_db = mongo_client['customer-keep-track']

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_db = int(os.getenv('REDIS_DB', 0))
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

conn = psycopg2.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    port=os.getenv("PORT"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("NAME")
)
cursor = conn.cursor()

def execute_query(query, values):
    global cursor, conn
    try:
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        conn.rollback()