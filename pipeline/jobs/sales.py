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
from pyflink.common import Types, WatermarkStrategy
from dotenv import load_dotenv
import pandas as pd
import logging
from time import sleep
# Load environment variables
load_dotenv()
KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
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

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

def get_holiday(date):
    vn_holidays = holidays.Vietnam()
    holiday = vn_holidays.get(date)
    if not holiday:
        return "Normal Day"
    return holiday

def parse_date(date_str: str) -> dict:
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

def configure_source(topic: str, earliest: bool = False) -> KafkaSource:
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
    
    def get_columns(self, table_name):
        try:
            self.cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}'".format(table_name=table_name))
            cols = [i[0] for i in self.cursor.fetchall()]
            return cols
        except Exception as e:
            self.cursor.execute("ROLLBACK")
    
    def get_all_table(self,):
        try:
            self.cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            tables = [i[0] for i in self.cursor.fetchall()]
            return tables
        except Exception as e:
            self.cursor.execute("ROLLBACK")
    
    def delete_table(self, table_names = []):
        for table in table_names:
            try:
                self.cursor.execute(f"DROP TABLE {table}")
                print(f"🗑 Deleted {table}")
            except Exception as e:
                self.cursor.execute("ROLLBACK")
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
    
    def delete(self, table_name, pk_id):
        try:
            self.cursor.execute(f"DELETE FROM {table_name} WHERE id={pk_id};")
            self.conn.commit()
        except Exception as e:
            self.cursor.execute("ROLLBACK")
    
    def truncate(self, table_name):
        try:
            self.cursor.execute(f"TRUNCATE {table_name} CASCADE")
            self.conn.commit()
        except Exception as e:
            self.cursor.execute("ROLLBACK")

def stream_orders(message: str):
    """Process and sink data into PostgreSQL and ClickHouse for 'orders' topic."""
    logger.info(f"\n⌛️ [Orders] processing ...")
    try:
        mode, data = decode_message(message)
        status = data.get('order_status')
        order_id = data.get('order_id')
        customer_id = data.get('customer_id')
        order_date = data.get('order_date')
        date_row = parse_date(datetime.strptime(order_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d"))
        full_date = date_row['full_date']
        row = (order_id, status, order_date, customer_id)
        if not data:
            logger.warning("\n⚪️ [Orders] No data to process.")
            return
        if status not in ['completed', 'cancelled']:
            logger.info("\n⚪️ [Orders] not finish.")
            return
        pg = Postgres()
        # Insert or update order in PostgreSQL
        if mode != "Delete": 
            pg.upsert(
                data=row,
                table_name='orders',
                conflict_target='id'
            )
            logger.info(f"\n🟢 [Orders] Upsert into PostgreSQL: {row}")
            
            df_date = pg.query(f"SELECT * FROM order_date WHERE full_date='{full_date}' LIMIT 1;")
            if df_date.empty:
                # Chuyển đổi chuỗi ngày ('2024-12-16') thành đối tượng datetime
                date_row = list(date_row.values())
                date_str = date_row[1]
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                # Thay thế giá trị chuỗi ngày bằng đối tượng datetime
                date_row[1] = date_obj
                # Bây giờ date_row đã được chuẩn hóa với kiểu dữ liệu datetime cho 'full_date'
                client = get_clickhouse_client()
                client.insert('dim_date', [date_row], column_names=['id', 'full_date', 'day', 'month', 'year', 'quarter', 'day_of_week', 'week_of_year', 'is_weekend', 'is_holiday'])
                client.close()
                logger.info(f"\n🟢 [Dim_Date] Inserted into Clickhouse: {date_row}")
            else:
                logger.info(f"\n⚪️ [Dim_Date] Exist data in order_date: {date_row}")
            
            pg.upsert(
                data=date_row,
                table_name='order_date',
                conflict_target='id'
            )
            logger.info(f"\n🟢 [Order_date] Upsert into PostgreSQL: {date_row}")
        pg.close()
    except Exception as e:
        logger.error(f"\n❌ [Orders | Dim_Date] Error processing message: {e}")
    print('\n' + '-'*120)

def stream_order_products(message: str):
    """Process and sink data into ClickHouse for 'order_products' topic."""
    sleep(5)
    logger.info(f"\n⌛️ [Order Products] processing ...")
    query_sales = '''
        SELECT 
            op.id, 
            op.quantity, 
            op.total_amount, 
            o.status, 
            o.order_date,
            pp.id as promotion_id,
            pr.id AS location_id,
            p.id AS product_id,
            c.id AS customer_id, 
            s.id AS shop_id
        FROM order_product op 
        LEFT JOIN orders o ON o.id = op.order_id
        LEFT JOIN product p ON p.id = op.product_id
        LEFT JOIN promotion_product pp ON pp.product_id = p.id
        LEFT JOIN customer c ON c.id = o.customer_id
        LEFT JOIN users u ON u.id = c.user_id
        LEFT JOIN address ad ON ad.id = u.address_id
        LEFT JOIN province pr ON pr.id = ad.province_id
        LEFT JOIN store s ON s.id = p.shop_id
        WHERE op.id = {op_id}
        GROUP BY op.id, op.quantity, op.total_amount, o.status, o.order_date, pp.id, pr.id, p.id, o.id, c.id, s.id;
    '''
    try:
        pg = Postgres()
        mode, data = decode_message(message)
        if not data:
            logger.warning("\n⚪️ [Order Products] No data to process.")
            return
        id = data.get("order_product_id")
        order_id = data.get('order_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        price = data.get('price')
        row = (id, quantity, price, order_id, product_id)
        
        if mode != "Delete":
            pg.upsert(
                data=row,
                table_name='order_product',
                conflict_target='id'
            )
            logger.info(f"\n🟢 [Order_Product] Upsert into PostgreSQL: {row}")
        
        df_sales = pg.query(query_sales.format(op_id=id), fetch=True)
        if not df_sales.empty:
            df_sales = list(df_sales.values[-1])
            date_obj = df_sales[4]
            df_sales[4] = parse_date(date_obj.strftime('%Y-%m-%d'))['id']
            client = get_clickhouse_client()
            client.insert('fact_sales', [df_sales], column_names=['id', 'quantity', 'total_amount', 'status', 'date_id', 'promotion_id', 'location_id', 'product_id', 'customer_id', 'shop_id'])
            client.close()
            logger.info(f"\n🟢 [Order_Products] Inserted into ClickHouse: {df_sales}")
        else:
            logger.warning(f"\n⚪️ [Order_Products] Not found order_product_id {id}")
        
        pg.close()

    except Exception as e:
        logger.error(f"\n❌ [Order_Products] Error processing message: {e}")
    print('\n' + '-'*120)

def main() -> None:
    """Main flow controller"""
    env = initialize_env()
    
    # Configure Kafka sources for both topics
    kafka_source_orders = configure_source(topic='postgresDB.public.orders')
    kafka_source_order_products = configure_source(topic='postgresDB.public.order_products')
    
    # Create data streams from each Kafka source
    data_stream_orders = env.from_source(
        kafka_source_orders, 
        WatermarkStrategy.no_watermarks(), 
        "Kafka orders topic"
    )
    
    data_stream_order_products = env.from_source(
        kafka_source_order_products, 
        WatermarkStrategy.no_watermarks(), 
        "Kafka order_products topic"
    )
    
    # Map each stream to its respective processing function
    data_stream_orders.map(
        stream_orders,
        output_type=Types.STRING()
    )   
    
    data_stream_order_products.map(
        stream_order_products,
        output_type=Types.STRING()
    )
    
    # Execute the Flink job
    env.execute("Stream ingest sales job")

if __name__ == "__main__":
    main()
