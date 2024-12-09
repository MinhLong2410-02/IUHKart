from datetime import datetime, timedelta
from airflow import AirflowException
from airflow.decorators import dag, task

import psycopg2
import random
import os
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
load_dotenv(".env")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")
POSTGRES_PORT=os.getenv("POSTGRES_PORT")
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB=os.getenv("POSTGRES_DB")

def _get_length(conn, table_name):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        length = cursor.fetchone()[0]
    return length

def _generate_random_id(conn, table_name, pk_name):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT {pk_name} FROM {table_name}")
        customer_ids = cursor.fetchall()
    return random.choice(customer_ids)[0]

def _load_to_df(conn, table_name):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
    return pd.DataFrame(data, columns=columns)

def _get_price(conn, product_id):
    df_p = _load_to_df(conn, 'products')
    df_pd = _load_to_df(conn, 'order_product_discounts')
    df_d = _load_to_df(conn, 'discounts')
    price = df_p[df_p['product_id'] == product_id]['original_price'].values[0]
    discount_id = df_pd[df_pd['product_id'] == product_id]
    if len(discount_id) == 0:
        return price
    discount_id = discount_id['discount_id'].values[0]
    discount = df_d[df_d['discount_id'] == discount_id]
    discount = discount['discount_percent'].values[0]
    return price * (1 - discount / 100)

def insert_order(conn):
    """Hàm chèn dữ liệu ngẫu nhiên vào bảng test."""
    try:
        # Lấy ngẫu nhiên id từ bảng customers
        customer_id = _generate_random_id(conn, "customers", "id")

        # Lấy ngẫu nhiên id từ bảng products
        product_id = _generate_random_id(conn, "products", "product_id")

        # Lấy ngẫu nhiên id 
        address_id = _generate_random_id(conn, "addresses", "address_id")

        # Tạo dữ liệu ngẫu nhiên
        order_id = _get_length(conn, "orders") + 1
        order_number = order_id
        shipping_date = datetime.now()
        order_date = datetime.now()
        order_status = random.choices(['completed', 'completed', 'completed', 'completed', 'completed', 'completed', 'cancelled'])[0]

        # order_product
        order_product_id = order_id
        quantity = random.randint(1, 3)
        price = _get_price(conn, product_id) * quantity
        order_total = price

        # transaction
        transaction_id = order_id
        transaction_date = datetime.now()
        transaction_amount = price
        transaction_status = 'completed' if order_status == 'completed' else 'failed'
        
        insert_order = """
            INSERT INTO orders (order_id, order_number, shipping_date, order_date, order_status, order_total, address_id, customer_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        insert_order_product = """
            INSERT INTO order_products (order_product_id, quantity, price, order_id, product_id)
            VALUES (%s, %s, %s, %s, %s);
        """
        insert_transaction = """
            INSERT INTO transactions (transaction_id, transation_date, total_money, status, customer_id, order_id)   
            VALUES (%s, %s, %s, %s, %s, %s);
        """

        with conn.cursor() as cursor:
            cursor.execute(insert_order, (order_id, order_number, shipping_date, order_date, order_status, order_total, address_id, customer_id))
            cursor.execute(insert_order_product, (order_product_id, quantity, price, order_id, product_id))
            cursor.execute(insert_transaction, (transaction_id, transaction_date, transaction_amount, transaction_status, customer_id, order_id))
        conn.commit()
        print(f"Đã chèn dữ liệu order_id={order_id} vào bảng orders.")

    except psycopg2.IntegrityError as e:
        conn.rollback()
        raise (f"Lỗi IntegrityError: {e}")
    except Exception as e:
        conn.rollback()
        raise (f"Đã xảy ra lỗi: {e}")

def main():
    # Cấu hình kết nối tới PostgreSQL
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    print("✅ Kết nối tới PostgreSQL thành công.")

    insert_order(conn)

@dag(
    dag_id='generate_orders',
    start_date=datetime(2024, 11, 25),
    schedule=timedelta(seconds=10),
    catchup=False,
)
def order():
    @task(retries=5, retry_delay=timedelta(minutes=5))
    def generate_order():
        main()

    generate_order()


order()