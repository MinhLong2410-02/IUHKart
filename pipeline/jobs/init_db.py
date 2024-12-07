import clickhouse_connect
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE")

def create_tables(client):
    with open("schema.sql", 'r') as f:
        schema = f.read()
    create_commands = schema.split('\n\n')
    
    for command in create_commands:
        try:
            client.command(command)
            print(f'✅ successfully.')
        except Exception as e:
            print(f"❌ Error executing command: {e}")

# insert data csv
def insert_data(client, table_name):
    try:
        df = pd.read_csv(f'db/{table_name}.csv')
        for col_name in ["date_of_birth", "signup_date", "establish_date"]:
            if col_name in df.columns:
                df[col_name] = pd.to_datetime(df[col_name], errors='coerce')

        data = [tuple(x) for x in df.to_numpy()]
        # Chèn dữ liệu vào ClickHouse
        client.insert(
            table_name,
            data,
            column_names=df.columns
        )
        print(f"✅ Insert data to {table_name} successfully.")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    # Kết nối tới ClickHouse
    client = clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DATABASE
    )

    # Tạo các bảng
    # create_tables(client)
    insert_data(client, 'dim_product')
    insert_data(client, 'dim_customer')
    insert_data(client, 'dim_store')
    insert_data(client, 'dim_promotion')
    client.close()

if __name__ == "__main__":
    main()