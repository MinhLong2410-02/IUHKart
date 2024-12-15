from datetime import datetime, timedelta
from airflow import AirflowException
from airflow.decorators import dag, task

import psycopg2
import random
import os
from datetime import datetime
from pytz import timezone
from faker import Faker
fake = Faker()


def _generate_random_id(list_id):
    return random.choice(list_id)

def _load_ids(conn, table_name, pk_name):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT {pk_name} FROM {table_name}")
        data = cursor.fetchall()
    return data

def insert_product(conn):
    attributes = ["product_id", "product_name", "original_price", "stock", "brand", "slug", "product_description", "date_created", "ratings", "date_add", "category_id", "vendor_id"]
    id_categories = _load_ids(conn, "categories", "category_id")
    id_vendors = _load_ids(conn, "vendors", "id")
    
    category_id = _generate_random_id(id_categories)
    vendor_id = _generate_random_id(id_vendors)
    product_name = fake.slug()
    original_price = random.randint(10000, 500000)
    stock = random.randint(0, 100)
    brand = fake.company()
    slug = product_name
    product_description = fake.text()
    date_created = datetime.now(tz=timezone('Asia/Ho_Chi_Minh')).strftime('%Y-%m-%d %H:%M:%S')
    ratings = random.randint(1, 5)
    date_add = datetime.now(tz=timezone('Asia/Ho_Chi_Minh')).strftime('%Y-%m-%d %H:%M:%S')
    
    insert_product = """
        INSERT INTO products (product_name, original_price, stock, brand, slug, product_description, date_created, ratings, date_add, category_id, vendor_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    with conn.cursor() as cursor:
        cursor.execute(insert_product, (product_name, original_price, stock, brand, slug, product_description, date_created, ratings, date_add, category_id, vendor_id))
    conn.commit()
    print(f"Đã chèn dữ liệu thành công")

def main():
    # Cấu hình kết nối tới PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    print("✅ Kết nối tới PostgreSQL thành công.")

    with conn.cursor() as cursor:
        cursor.execute("SELECT pg_get_serial_sequence('products', 'product_id');")
        sequence_name = cursor.fetchone()[0]
        cursor.execute(f"SELECT setval('{sequence_name}', COALESCE((SELECT MAX(product_id) FROM products), 1), true);")
        conn.commit()

    insert_product(conn)

@dag(
    dag_id='generate_product',
    start_date=datetime(2024, 11, 25),
    schedule=timedelta(seconds=30),
    catchup=False
)
def generate():
    @task(retries=5, retry_delay=timedelta(minutes=5))
    def generate_product():
        main()
    generate_product()

generate()