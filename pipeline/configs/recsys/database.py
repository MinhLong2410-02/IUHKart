from psycopg2 import pool
from pymongo import MongoClient
from qdrant_client import QdrantClient
from configs import *
import sys

# MongoDB connection setup
mongo_client = MongoClient(CONNECTION_STRING)
db = mongo_client["tracking_db"]

# Qdrant client setup
qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# PostgreSQL connection pooling setup
# Define a global connection pool
postgres_pool = None

def init_postgres_pool():
    global postgres_pool
    if postgres_pool is None:
        postgres_pool = pool.SimpleConnectionPool(
            1,  # Minimum number of connections in the pool
            10,  # Maximum number of connections in the pool
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB
        )
        print("🟢 PostgreSQL connection pool initialized.")
        sys.stdout.flush()

def get_postgres_connection():
    # Get a connection from the pool
    if postgres_pool is None:
        init_postgres_pool()
    return postgres_pool.getconn()

def release_postgres_connection(conn):
    # Return the connection to the pool
    if postgres_pool is not None:
        postgres_pool.putconn(conn)

# Ensure proper connection pool handling
def execute_query(query, params=None):
    conn = None
    try:
        conn = get_postgres_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()  # Commit the transaction if needed
            return cursor.fetchall()  # Return results if query returns anything
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        if conn:
            release_postgres_connection(conn)

def close_postgres_pool():
    # Close the connection pool when the application shuts down
    if postgres_pool is not None:
        postgres_pool.closeall()

def update_recommendations_in_postgres(user_id: str, recommended_product_ids: list):
    """
    Updates the recommend_product_ids column in the customers table for the given user_id.
    """
    query = """
        UPDATE customers
        SET recommend_product_ids = %s
        WHERE user_id = %s
    """
    params = (recommended_product_ids, user_id)
    
    try:
        # Use the execute_query function to handle the query
        execute_query(query, params)
        print(f"🟢 Updated recommendations for user {user_id}: {recommended_product_ids}")
        sys.stdout.flush()
    except Exception as e:
        print(f"Error updating recommendations for user {user_id}: {e}")

# Initialize the connection pool when the script starts
init_postgres_pool()
