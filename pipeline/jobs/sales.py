import json
from pyflink.common import Types, Time
from pyflink.datastream.functions import KeyedProcessFunction, RuntimeContext
from pyflink.datastream.state import ValueStateDescriptor, StateTtlConfig
from utils import initialize_env, configure_source, get_clickhouse_client, decode_message
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class DeduplicationProcessFunction(KeyedProcessFunction):
    """ProcessFunction để thực hiện deduplication dựa trên review_id."""

    def __init__(self):
        self.review_id_state = None
        self.clickhouse_client = None

    def open(self, runtime_context: RuntimeContext):
        # Thiết lập state descriptor với TTL 1 ngày
        
        ttl_config = (
            StateTtlConfig
            .new_builder(Time.days(1))
            .set_update_type(StateTtlConfig.UpdateType.OnCreateAndWrite)
            .build()
        )
        descriptor = ValueStateDescriptor("review_id_state", Types.BOOLEAN())
        descriptor.enable_time_to_live(ttl_config)
        self.review_id_state = runtime_context.get_state(descriptor)

        # Khởi tạo ClickHouse client
        self.clickhouse_client = get_clickhouse_client()

    def process_element(self, value, ctx: 'KeyedProcessFunction.Context'):
        """
        Xử lý từng phần tử trong stream.
        value: Chuỗi JSON từ Kafka
        """
        mode, data = decode_message(value)
        if not data:
            logger.warning("No data extracted from message.")
            return

        review_id = data.get('review_id')
        if not review_id:
            logger.warning("No review_id found in message.")
            return

        # Kiểm tra xem review_id đã tồn tại trong state chưa
        seen = self.review_id_state.value()
        if seen:
            # Đã thấy trong state, bỏ qua
            logger.info(f"Duplicate review_id {review_id} found in state. Skipping.")
            return

        # Nếu chưa thấy trong state, kiểm tra trong ClickHouse
        try:
            query = f"SELECT COUNT(*) FROM fact_review WHERE id = %(id)s"
            result = self.clickhouse_client.query(query, {"id": review_id})
            count = result.result_set[0][0]
            if count > 0:
                logger.info(f"Duplicate review_id {review_id} found in ClickHouse. Skipping.")
                return
        except Exception as e:
            logger.error(f"Error querying ClickHouse for review_id {review_id}: {e}")
            return

        # Nếu chưa tồn tại, chèn vào ClickHouse và cập nhật state
        try:
            content = data.get('review_content')
            rating = data.get('review_rating')
            date_id = data.get('review_date')
            product_id = data.get('product_id_id')
            customer_id = data.get('customer_id_id')

            row = (review_id, content, rating, date_id, product_id, customer_id)

            self.clickhouse_client.insert(
                'fact_review',
                [row],
                column_names=['id', 'content', 'rating', 'date_id', 'product_id', 'customer_id']
            )

            # Cập nhật state để đánh dấu review_id đã được xử lý
            self.review_id_state.update(True)

            logger.info(f"🟢 Inserted into ClickHouse: {row}")

        except Exception as e:
            logger.error(f"❌ Error inserting review_id {review_id} into ClickHouse: {e}")

    def close(self):
        if self.clickhouse_client:
            self.clickhouse_client.close()

def main() -> None:
    """Main flow controller"""

    # Initialize environment
    env = initialize_env()
    logger.info("🟢 Initializing environment")

    # Define source
    kafka_source = configure_source(f"{KAFKA_HOST}:{KAFKA_PORT}", KAFKA_HEAD_TOPIC)
    logger.info("🟢 Configuring Kafka source")

    data_stream = env.from_source(
        kafka_source, WatermarkStrategy.no_watermarks(), "Kafka reviews topic"
    )
    logger.info("🟢 Created DataStream from Kafka source")

    # Áp dụng deduplication
    dedup_stream = (
        data_stream
        .key_by(lambda msg: json.loads(msg).get('review_id'))
        .process(DeduplicationProcessFunction(), output_type=Types.VOID())
    )
    logger.info("🟢 Applied deduplication ProcessFunction")

    # Thực thi job Flink
    env.execute("Flink ETL Job with Deduplication")

if __name__ == "__main__":
    main()