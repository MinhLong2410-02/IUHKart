from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.functions import KeyedBroadcastProcessFunction, RuntimeContext
from pyflink.common.typeinfo import Types
from pyflink.common import WatermarkStrategy, Time
import json
from clickhouse_driver import Client

class CategoryBroadcastFunction(KeyedBroadcastProcessFunction):
    def __init__(self):
        self.category_state = None

    def open(self, runtime_context: RuntimeContext):
        self.category_state = runtime_context.get_state(
            state_descriptor=Types.PICKLED_BYTE_ARRAY()
        )

    def process_element(self, value, ctx: 'KeyedBroadcastProcessFunction.Context', out):
        # value: product record
        product = json.loads(value)
        category_id = product.get('category_id')
        category_name = self.category_state.value().get(category_id, 'Unknown')
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
        # value: category record
        category = json.loads(value)
        category_id = category.get('id')
        category_name = category.get('name')
        current_state = self.category_state.value()
        if current_state is None:
            current_state = {}
        current_state[category_id] = category_name
        self.category_state.update(current_state)

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)  # Tùy chỉnh theo nhu cầu
    env.set_stream_time_characteristic(TimeCharacteristic.ProcessingTime)

    # Kafka consumer properties
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
    broadcast_stream = category_stream.broadcast(Types.PICKLED_BYTE_ARRAY())

    # Kết hợp product stream với broadcast category stream
    enriched_stream = product_stream.connect(broadcast_stream).process(CategoryBroadcastFunction(), output_type=Types.STRING())

    # Sink vào ClickHouse
    enriched_stream.add_sink(ClickHouseSink())

    # Thực thi job
    env.execute("Flink ETL Job with Broadcast State")

class ClickHouseSink:
    def __init__(self):
        self.client = None

    def open(self, runtime_context: RuntimeContext):
        self.client = Client(host='clickhouse', port=8123, user='default', password='')

    def invoke(self, value, context):
        # value là JSON string đã được enriched
        record = json.loads(value)
        self.client.execute(
            'INSERT INTO product (id, name, brand, price, stock, category) VALUES',
            [(record['id'], record['name'], record['brand'], record['price'], record['stock'], record['category'])]
        )

    def close(self):
        if self.client:
            self.client.disconnect()

if __name__ == '__main__':
    main()