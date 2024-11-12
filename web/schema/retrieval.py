import psycopg2
import pandas as pd

# Thông tin kết nối tới PostgreSQL
conn_info = {
    "host": "crawl.serveftp.com",
    "port": "5567",
    "database": "postgres",
    "user": "iuhkart",
    "password": "iuhkartpassword"
}

# Hàm kết nối và lấy dữ liệu từ bảng
def fetch_data_from_db(query, conn_info):
    try:
        # Kết nối tới cơ sở dữ liệu
        conn = psycopg2.connect(**conn_info)
        cursor = conn.cursor()

        # Thực hiện truy vấn
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()

        # Đóng kết nối
        cursor.close()
        conn.close()

        # Chuyển kết quả thành DataFrame
        df = pd.DataFrame(data, columns=columns)
        return df

    except Exception as e:
        print("Đã xảy ra lỗi:", e)
        return None

# Truy vấn dữ liệu từ bảng `customers` và `addresses`
query_customers = "SELECT * FROM customers;"
query_addresses = "SELECT * FROM addresses;"

# Lấy dữ liệu
customers_df = fetch_data_from_db(query_customers, conn_info)
addresses_df = fetch_data_from_db(query_addresses, conn_info)


customers_df.to_csv('./data/customers.csv', index=False)
addresses_df.to_csv('./data/addresses.csv', index=False)
