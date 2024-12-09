USE default;

-- -- users table
-- CREATE TABLE IF NOT EXISTS users
-- (
--     id UInt32,
--     is_customer Boolean,
--     is_seller Boolean,
--     address_id UInt32,
--     ttl DateTime DEFAULT now()
-- )
-- ENGINE MergeTree
-- ORDER BY (id)
-- TTL ttl + INTERVAL 1 DAY;

-- CREATE TABLE IF NOT EXISTS _kafka_users
-- (
--     `message` String
-- )
-- ENGINE Kafka
-- SETTINGS
--     kafka_broker_list = 'kafka-postgres:9092',
--     kafka_topic_list = 'postgresDB.public.users',
--     kafka_group_name = 'clickhouse_user_consumer',
--     kafka_format = 'JSONAsString',
--     kafka_num_consumers = 1,
--     kafka_max_block_size = 1048576;

-- reviews table
CREATE TABLE IF NOT EXISTS reviews
(
    review_id UInt32,
    review_content LowCardinality(String),
    review_rating UInt32,
    review_date Datetime64(6),
    customer_id_id UInt32,
    product_id_id UInt32,
    ttl DateTime DEFAULT now()
)
ENGINE MergeTree
ORDER BY (review_rating)
TTL ttl + INTERVAL 1 DAY;

CREATE TABLE IF NOT EXISTS _kafka_reviews
(
    `message` String
)
ENGINE Kafka
SETTINGS
    kafka_broker_list = 'kafka-postgres:9092',
    kafka_topic_list = 'postgresDB.public.reviews',
    kafka_group_name = 'clickhouse_review_consumer',
    kafka_format = 'JSONAsString',
    kafka_num_consumers = 1,
    kafka_max_block_size = 1048576;

CREATE MATERIALIZED VIEW IF NOT EXISTS mv_reviews to reviews AS
SELECT
    JSONExtractUInt(message, 'after.review_id') AS review_id,
    JSONExtractString(message, 'after.review_content') AS review_content,
    JSONExtractUInt(message, 'after.review_rating') AS review_rating,
    parseDateTime64BestEffort(JSONExtractString(message, 'after.review_date'), 6) AS review_date,
    JSONExtractUInt(message, 'after.customer_id_id') AS customer_id_id,
    JSONExtractUInt(message, 'after.product_id_id') AS product_id_id
FROM _kafka_reviews
SETTINGS stream_like_engine_allow_direct_select = 1;