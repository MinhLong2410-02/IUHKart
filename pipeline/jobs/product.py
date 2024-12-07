from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.functions import KeyedBroadcastProcessFunction, RuntimeContext, SinkFunction
from pyflink.common.typeinfo import Types
from pyflink.datastream.state import MapStateDescriptor
import json
import clickhouse_connect

# Định nghĩa descriptor cho broadcast state
CATEGORY_STATE_DESCRIPTOR = MapStateDescriptor(
    "category_state",
    Types.INT(),   # category_id
    Types.STRING()  # category_name
)

class EnrichProductWithCategory(KeyedBroadcastProcessFunction):
    def __init__(self, initial_categories):
        self.initial_categories = initial_categories

    def open(self, runtime_context: RuntimeContext):
        # Initialize broadcast state with initial categories
        broadcast_state = runtime_context.get_broadcast_state(CATEGORY_STATE_DESCRIPTOR)
        for category_id, category_name in self.initial_categories.items():
            broadcast_state.put(category_id, category_name)

    def process_element(self, value, ctx: 'KeyedBroadcastProcessFunction.Context', out):
        # Xử lý record sản phẩm
        product = json.loads(value)
        category_id = product.get('category_id')
        broadcast_state = ctx.get_broadcast_state(CATEGORY_STATE_DESCRIPTOR)
        category_name = broadcast_state.get(category_id)
        if not category_name:
            category_name = "Unknown"  # Hoặc thực hiện truy vấn ClickHouse để lấy lại category_name
        enriched_product = {
            'id': product.get('id'),
            'name': product.get('name'),
            'brand': product.get('brand'),
            'price': product.get('price'),
            'stock': product.get('stock'),
            'category': category_name
        }
        out.collect(json.dumps(enriched_product))

    def process_broadcast_element(self, value, ctx: 'KeyedBroadcastProcessFunction.Context', out):
        # Cập nhật broadcast state với record danh mục mới
        category = json.loads(value)
        category_id = category.get('id')
        category_name = category.get('name')
        broadcast_state = ctx.get_broadcast_state(CATEGORY_STATE_DESCRIPTOR)
        broadcast_state.put(category_id, category_name)

class ClickHouseSink(SinkFunction):
    def __init__(self, host, port, username, password, database, table, batch_size=1000, flush_interval=2000):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.table = table
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.client = None
        self.buffer = []
        self.last_flush_time = None

    def open(self, runtime_context: RuntimeContext):
        self.client = clickhouse_connect.get_client(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database
        )
        self.last_flush_time = runtime_context.get_current_processing_time()

    def invoke(self, value, context):
        # value là JSON string đã được enriched
        record = json.loads(value)
        self.buffer.append((
            record['id'],
            record['name'],
            record['brand'],
            record['price'],
            record['stock'],
            record['category']
        ))

        current_time = context.timestamp()
        if len(self.buffer) >= self.batch_size or (current_time - self.last_flush_time) >= self.flush_interval:
            if self.buffer:
                self.client.insert(
                    self.table,
                    [
                        {'id': r[0], 'name': r[1], 'brand': r[2], 'price': r[3], 'stock': r[4], 'category': r[5]}
                        for r in self.buffer
                    ]
                )
                self.buffer = []
                self.last_flush_time = current_time

    def close(self):
        if self.buffer:
            self.client.insert(
                self.table,
                [
                    {'id': r[0], 'name': r[1], 'brand': r[2], 'price': r[3], 'stock': r[4], 'category': r[5]}
                    for r in self.buffer
                ]
            )
        if self.client:
            self.client.close()

def load_initial_categories(clickhouse_client):
    # Tải toàn bộ dữ liệu category từ ClickHouse
    categories = clickhouse_client.query("SELECT id, name FROM category")
    category_dict = {category['id']: category['name'] for category in categories}
    return category_dict

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)  # Tùy chỉnh theo nhu cầu
    env.set_stream_time_characteristic(TimeCharacteristic.ProcessingTime)

    # Kết nối với ClickHouse để tải dữ liệu category ban đầu
    clickhouse_client = clickhouse_connect.get_client(
        host='clickhouse',
        port=8123,
        username='default',
        password='',
        database='default'
    )
    initial_categories = load_initial_categories(clickhouse_client)
    clickhouse_client.close()

    # Cấu hình Kafka consumer
    kafka_props = {
        'bootstrap.servers': 'kafka-postgres:9092',
        'group.id': 'flink'
    }

    # Consumer cho products
    product_consumer = FlinkKafkaConsumer(
        topics='postgresDB.public.products',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    # Consumer cho categories
    category_consumer = FlinkKafkaConsumer(
        topics='postgresDB.public.categories',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    # Tiêu thụ dữ liệu từ Kafka
    product_stream = env.add_source(product_consumer)
    category_stream = env.add_source(category_consumer)

    # Broadcast category stream
    broadcast_stream = category_stream.broadcast(CATEGORY_STATE_DESCRIPTOR)

    # Kết hợp product stream với broadcast category stream
    enriched_stream = product_stream.key_by(lambda x: json.loads(x).get('category_id')) \
        .connect(broadcast_stream) \
        .process(EnrichProductWithCategory(initial_categories), output_type=Types.STRING())

    # Sink enriched stream vào ClickHouse
    enriched_stream.add_sink(
        ClickHouseSink(
            host='clickhouse',
            port=8123,
            username='default',
            password='',
            database='default',
            table='product'
        )
    )

    # Thực thi job
    env.execute("Flink ETL Job with Broadcast State and clickhouse_connect")

if __name__ == '__main__':
    main()