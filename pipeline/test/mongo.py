from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError

def connect_to_mongodb():
    connection_string = "mongodb://crawl.serveftp.com:27017/?replicaSet=rs0" #f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_db}&replicaSet={replica_set}"
    try:
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        # Kiểm tra kết nối
        client.admin.command('ping')
        print("Kết nối thành công tới MongoDB!")
        return client
    except ConnectionFailure:
        print("Không thể kết nối tới MongoDB. Vui lòng kiểm tra cấu hình và trạng thái của MongoDB.")
    except ConfigurationError as ce:
        print("Lỗi cấu hình:", ce)
    except Exception as e:
        print("Đã xảy ra lỗi:", e)
    return None

def list_databases(client):
    try:
        databases = client.list_database_names()
        print("Danh sách cơ sở dữ liệu:")
        for db in databases:
            print(f" - {db}")
    except Exception as e:
        print("Lỗi khi liệt kê cơ sở dữ liệu:", e)

def main():
    # Kết nối tới MongoDB
    client = connect_to_mongodb()
    if client:
        # Liệt kê các cơ sở dữ liệu
        list_databases(client)

        # Ví dụ: Truy cập vào một cơ sở dữ liệu cụ thể
        db_name = 'demo'  # Thay bằng tên cơ sở dữ liệu của bạn
        db = client[db_name]

        # Thêm một bản ghi vào bộ sưu tập 'user'
        collection = db['items']
        collection.insert_one({'name': 'qxnam', 'age': 22})
        print("📝 Đã thêm một bản ghi vào bộ sưu tập 'user'.")
        # Liệt kê các bộ sưu tập trong cơ sở dữ liệu
        try:
            collections = db.list_collection_names()
            print(f"Danh sách bộ sưu tập trong cơ sở dữ liệu '{db_name}':")
            for coll in collections:
                print(f" - {coll}")
        except Exception as e:
            print(f"Lỗi khi liệt kê bộ sưu tập trong cơ sở dữ liệu '{db_name}':", e)

if __name__ == "__main__":
    main()
