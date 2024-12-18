import pandas as pd
from utils import get_clickhouse_client

def drop_all_tables(client):
    try:
        # Lấy danh sách tất cả các bảng trong cơ sở dữ liệu hiện tại
        tables = client.query("SHOW TABLES").result_rows
        if not tables:
            print("Không có bảng nào để xóa.")
            return
        # Xóa từng bảng
        for table in tables:
            table_name = table[0]
            try:
                client.command(f"DROP TABLE IF EXISTS `{table_name}`")
                print(f"🟢 Đã xóa bảng: {table_name}")
            except Exception as e:
                print(f"❌ Lỗi khi xóa bảng {table_name}: {e}")
        print("🟢 Đã xóa tất cả các bảng thành công.")
    except Exception as e:
        print(f"❌ Lỗi khi lấy danh sách bảng: {e}")

def create_tables(client):
    with open("./clickhouse.sql", 'r') as f:
        schema = f.read()
    create_commands = schema.split('\n\n')
    for command in create_commands:
        try:
            client.command(command)
        except Exception as e:
            print(f"❌ Error executing command: {e}")
    print(f'✅ create all table successfully!')

# insert data csv
def insert_data(client, table_name):
    try:
        df = pd.read_csv(f'db/{table_name}.csv')
        for col_name in ["date_of_birth", "date_join", "date_post", "full_date"]:
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
    client = get_clickhouse_client()
    # Tạo các bảng
    drop_all_tables(client)
    create_tables(client)
    insert_data(client, 'dim_province')
    insert_data(client, 'dim_product')
    insert_data(client, 'dim_customer')
    insert_data(client, 'dim_store')
    insert_data(client, 'dim_promotion')
    insert_data(client, 'dim_date')
    insert_data(client, 'fact_sales')
    insert_data(client, 'fact_review')
    client.close()

if __name__ == "__main__":
    main()