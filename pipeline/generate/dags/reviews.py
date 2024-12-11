from datetime import datetime, timedelta
from pytz import timezone
from airflow import AirflowException
from airflow.decorators import dag, task

import psycopg2 
import random
import os
from faker import Faker
from dotenv import load_dotenv
load_dotenv(".env")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")
POSTGRES_PORT=os.getenv("POSTGRES_PORT")
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB=os.getenv("POSTGRES_DB")

def _generate_random_id(list_id):
    return random.choice(list_id)

def _generate_review_rating():
    return random.randint(1, 5)

def _generate_random_content():
    fake = Faker()
    return fake.text()

def insert_random_data(conn):
    """Hàm chèn dữ liệu ngẫu nhiên vào bảng test."""

    try:
        with conn.cursor() as cursor:
            
            # Lấy danh sách id từ bảng customer
            cursor.execute("SELECT id FROM customers")
            customer_ids = cursor.fetchall()
            customer_id = _generate_random_id(customer_ids)

            # Lấy danh sách id từ bảng product
            cursor.execute("SELECT product_id FROM products")
            product_ids = cursor.fetchall()
            product_id = _generate_random_id(product_ids)

            # Tạo dữ liệu ngẫu nhiên
            random_rating = _generate_review_rating()
            random_date = datetime.now(tz=timezone('Asia/Ho_Chi_Minh')).strftime('%Y-%m-%d %H:%M:%S')
            random_content = _generate_random_content()

            insert_query = """
                INSERT INTO reviews (review_rating, review_date, review_content, customer_id_id, product_id_id)
                VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (random_rating, random_date, random_content, customer_id, product_id))
            conn.commit()
            print(f"Đã chèn dữ liệu: {random_rating}, {random_date}, {customer_id}, {product_id}")
    except psycopg2.IntegrityError as e:
        # Xử lý lỗi vi phạm ràng buộc (ví dụ: trùng khóa chính)
        conn.rollback()
        raise (f"Lỗi IntegrityError: {e}")
    except Exception as e:
        # Xử lý các lỗi khác
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
    
    print("Kết nối tới PostgreSQL thành công.")
    
    with conn.cursor() as cursor:
        # Xác định sequence của bảng reviews
        # SELECT pg_get_serial_sequence('reviews', 'review_id');
        cursor.execute("SELECT pg_get_serial_sequence('reviews', 'review_id');")
        sequence_name = cursor.fetchone()[0]#.split('.')[-1]
        print(f"Sequence name: {sequence_name}")

        # Đồng bộ giá trị sequence với giá trị lớn nhất hiện có trong bảng
        cursor.execute(f"SELECT setval('{sequence_name}', COALESCE((SELECT MAX(review_id) FROM reviews), 1), true);")
        conn.commit()
    
    insert_random_data(conn)


@dag(
    dag_id='generate_review',
    start_date=datetime(2024, 11, 25),
    schedule=timedelta(seconds=30),
    catchup=False,
)
def review():
    @task(retries=5, retry_delay=timedelta(minutes=5))
    def generate_review():
        main()

    generate_review()


review()
