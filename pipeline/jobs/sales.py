from datetime import datetime
import holidays
import json, os
import clickhouse_connect
import psycopg2
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.kafka import (
    KafkaOffsetsInitializer,
    KafkaSource,
)
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
KAFKA_HEAD_TOPIC = os.getenv("KAFKA_HEAD_TOPIC")
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

def get_holiday(date):
    vn_holidays = holidays.Vietnam()
    holiday = vn_holidays.get(date)
    if not holiday:
        return "Normal Day"
    return holiday

def parse_date(date_str:str) -> dict:
    _id = int(date_str.replace('-', ''))
    date = datetime.strptime(date_str,  "%Y-%m-%d")
    return {
        'id': _id,
        'full_date': date_str,
        'day': date.day,
        'month': date.month,
        'year': date.year,
        'quarter': (date.month - 1) // 3 + 1,
        'day_of_week': date.weekday(),
        'week_of_year': date.isocalendar()[1],
        'is_weekend': date.weekday() in [5, 6],
        'is_holiday': get_holiday(date_str)
    }

def decode_message(message: str):
    """Decode Kafka message and extract change data."""
    try:
        message_json = json.loads(message)
        operation = message_json.get('op')
        before = {k.split(".")[-1]: v for k, v in message_json.items() if k.startswith('before') and k.split(".")[-1]}
        after = {k.split(".")[-1]: v for k, v in message_json.items() if k.startswith('after') and k.split(".")[-1]}
        if operation == 'c':
            return 'Create', after
        elif operation == 'u':
            return 'Update', after
        elif operation == 'r':
            return 'Read', after
        elif operation == 'd':
            return 'Delete', before
        else:
            return 'Unknown', None
    except Exception as e:
        print(f"🔻 Error decoding message: {e}")
        return None, None

def get_clickhouse_client():
    """Initialize ClickHouse client."""
    client = clickhouse_connect.get_client(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD,
        database=CLICKHOUSE_DATABASE,
    )
    return client

def initialize_env() -> StreamExecutionEnvironment:
    """Initializes the Flink stream execution environment."""
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(2)

    # Get current directory
    root_dir_list = __file__.split("/")[:-2]
    root_dir = "/".join(root_dir_list)

    # Adding the jar to the flink streaming environment
    env.add_jars(
        f"file://{root_dir}/lib/flink-sql-connector-kafka-3.1.0-1.18.jar",
    )
    return env

def configure_source(topic:str,  earliest:bool = False) -> KafkaSource:
    """Initializes Kafka source."""
    properties = {
        "bootstrap.servers": f"{KAFKA_HOST}:{KAFKA_PORT}",
        "group.id": f"flink_{topic.split('.')[-1]}_consumer",
    }

    offset = KafkaOffsetsInitializer.latest()
    if earliest:
        offset = KafkaOffsetsInitializer.earliest()

    kafka_source = (
        KafkaSource.builder()
        .set_topics(topic)
        .set_properties(properties)
        .set_starting_offsets(offset)
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )
    return kafka_source

class Postgres():
    def __init__(self):
        self.host = POSTGRES_HOST
        self.user = POSTGRES_USER
        self.port = POSTGRES_PORT
        self.password = POSTGRES_PASSWORD
        self.database = POSTGRES_DB
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            port=self.port,
            password=self.password
        )
        self.cursor = self.conn.cursor()
    
    def close(self):
        self.cursor.close()
        self.conn.close()

    def query(self, sql_query, fetch=True):
        try:
            self.cursor.execute(sql_query)
            self.conn.commit()
            if fetch:
                rows = self.cursor.fetchall()
                df = pd.DataFrame(rows, columns=[desc[0] for desc in self.cursor.description])
                return df
            return self.cursor.fetchall()
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f'❌ ROLLBACK: {e}')
    
    def create_schema(self, sql_path='*.sql'):
        with open(sql_path, 'r') as f:
            schema = f.read().split('\n\n')
        try:
            for statement in schema:
                self.cursor.execute(statement)
                if statement.find('CREATE TABLE') != -1:
                    print(f'''📢 Created table {statement.split('"')[1]}''')
                if statement.find('ALTER TABLE') != -1:
                    alter = statement.split('"')
                    print(f'''🔌 Linked table {alter[1]} -> {alter[5]}''')
            self.conn.commit()
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f'❌ ROLLBACK: {e}')
    
    def get_columns(self, table_name):
        try:
            self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}'".format(table_name=table_name))
            cols = [i[0] for i in self.cursor.fetchall()]
            return cols
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f'❌ ROLLBACK: {e}')
    
    def get_all_table(self,):
        try:
            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = [i[0] for i in self.cursor.fetchall()]
            return tables
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f'❌ ROLLBACK: {e}')
    
    def delete_table(self, table_names = []):
        for table in table_names:
            try:
                self.cursor.execute(f"DROP TABLE {table}")
                print(f"🗑 Deleted {table}")
            except Exception as e:
                self.cursor.execute("ROLLBACK")
                print(f'❌ ROLLBACK: {e}')
        self.conn.commit()
    
    def upsert(self, data, table_name, conflict_target:str='id', updates:list=None):
        try:
            cols = self.get_columns(table_name)
            _cols = [c for c in cols if c != conflict_target]
            if updates is None:
                updates = ','.join([f"{c}={'EXCLUDED.'+c}" for c in _cols])
            sql_insert = f"""
                INSERT INTO {table_name} ({','.join(cols)})
                VALUES ({','.join(['%s']*len(cols))})
                ON CONFLICT ({conflict_target})
                DO UPDATE SET {updates};
            """
            self.cursor.execute(sql_insert, data)
            self.conn.commit()
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f'❌ ROLLBACK: {e}')
            
    def upserts(self, datas, table_name, conflict_target:str='id', updates:list=None):
        try:
            cols = self.get_columns(table_name)
            _cols = [c for c in cols if c != conflict_target]
            if updates is None:
                updates = ','.join([f"{c}={'EXCLUDED.'+c}" for c in _cols])
            sql_insert = f"""
                INSERT INTO {table_name} ({','.join(cols)})
                VALUES ({','.join(['%s']*len(cols))})
                ON CONFLICT ({conflict_target})
                DO UPDATE SET {updates};
            """
            self.cursor.executemany(sql_insert, datas)
            self.conn.commit()
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f'❌ ROLLBACK: {e}')
    
    def delete(self, table_name, pk_id):
        try:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE id={pk_id};")
            self.conn.commit()
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f'❌ ROLLBACK: {e}')
    
    def truncate(self, table_name):
        try:
            self.cursor.execute(f"TRUNCATE {table_name} CASCADE")
            self.conn.commit()
        except Exception as e:
            self.cursor.execute("ROLLBACK")
            print(f'❌ ROLLBACK: {e}')

## ------------------------------------------------------------------------------
import json
import logging
from pyflink.common import Types, WatermarkStrategy
# from utils import *
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def stream_sales(message: json):
    """Process and sink data into ClickHouse."""
    logger.info(f"\n🚩 [sales] processing ...")
    try:
        pg = Postgres()
        mode, data = decode_message(message)
        df_o = pd.read_csv("Database/orders.csv")
        df_od = pd.read_csv("Database/order_products.csv")
        df_dis = pd.read_csv("Database/discounts.csv")
        df_pd = pd.read_csv("Database/product_discount.csv")
        df_p = pd.read_csv("Database/products.csv")
        df_ad = pd.DataFrame({
            'address_id': [1, 2, 3, 4],
            'province_id': [79, 79, 79, 79]
        })
        df_pro = pd.read_csv("https://raw.githubusercontent.com/MinhLong2410-02/VN-province-api-test/main/province.csv")
        df_a_p = pd.merge(df_ad,df_pro,on="province_id")
        province_map = df_a_p.set_index('address_id')['province_id'].to_dict()
        discount_map = df_pd.set_index('product_id')['discount_id'].to_dict()
        product_shop = df_p.set_index('product_id')['vendor_id'].to_dict()
        pg.close()
        
        df_sales = pd.merge(df_od, df_o, on='order_id')
        df_sales["date_id"] = df_sales["order_date"].apply(lambda x: parse_date(x)['id'])
        date = [parse_date(x) for x in df_sales['order_date']]
        df_sales["promotion_id"] = df_sales["product_id"].apply(lambda x: discount_map[x] if x in discount_map else None)
        df_sales["location_id"] = df_sales["customer_id"].apply(lambda x: province_map[x] if x in province_map else None)
        df_sales["shop_id"] = df_sales["product_id"].apply(lambda x: product_shop[x] if x in product_shop else None)
        df_sales = df_sales[["order_product_id", "quantity", "total_price", "order_status", "date_id", "promotion_id", "location_id", "product_id", "customer_id", "shop_id"]]
        df_sales.columns = ["id", "quantity", "total_amount", "status", "date_id", "promotion_id", "location_id", "product_id", "customer_id", "shop_id"]
        
        # Prepare data for ClickHouse
        row = (id, content, rating, date_post, product_id, customer_id, store_id)
        if mode == 'Create':
            client = get_clickhouse_client()
            client.insert('fact_sales', [row], column_names=['id', 'content', 'rating', 'date_post', 'product_id', 'customer_id', 'shop_id'])
            client.close()
        
        logger.info(f"\n🟢 [sales] Inserted into ClickHouse: {row}")

    except Exception as e:
        logger.error(f"\n❌ [sales] Error processing message: {e}")
    print('\n' + '-'*120)
    
def main() -> None:
    """Main flow controller"""
    env = initialize_env()
    kafka_source = configure_source(topic='postgresDB.public.saless')
    data_stream = env.from_source(
        kafka_source, WatermarkStrategy.no_watermarks(), "Kafka sensors topic 3"
    )
    data_stream.map(
        stream_sales,
        output_type=Types.STRING()
    )
    env.execute("Stream sales job")

if __name__ == "__main__":
    main()
