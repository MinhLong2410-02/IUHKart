USE default;

-- ------------------------------ Bảng customers
-- CREATE TABLE IF NOT EXISTS customers (
--     id UInt32,
--     fullname LowCardinality(String),
--     gender LowCardinality(String),
--     date_of_birth Datetime64(2),
--     date_join Datetime64(2),
--     user_id UInt32,
--     ttl DateTime DEFAULT now()
-- )
-- ENGINE MergeTree
-- ORDER BY (id)
-- TTL ttl + INTERVAL 1 DAY;

-- -- Bảng Kafka cho customers
-- CREATE TABLE IF NOT EXISTS _kafka_customers (
--     `message` String
-- )
-- ENGINE Kafka
-- SETTINGS
--     kafka_broker_list = 'kafka-postgres:19092',
--     kafka_topic_list = 'postgresDB.public.customers',
--     kafka_group_name = 'clickhouse_customer_consumer',
--     kafka_format = 'JSONAsString',
--     kafka_num_consumers = 1,
--     kafka_max_block_size = 1048576;

-- -- Materialized View để chuyển dữ liệu từ Kafka vào bảng customers
-- CREATE MATERIALIZED VIEW IF NOT EXISTS mv_customers TO customers AS
-- SELECT
--     JSONExtractUInt(message, 'after.id') AS id,
--     JSONExtractString(message, 'after.fullname') AS fullname,
--     JSONExtractString(message, 'after.gender') AS gender,
--     parseDateTime64BestEffort(JSONExtractString(message, 'after.date_of_birth'), 2) AS date_of_birth,
--     parseDateTime64BestEffort(JSONExtractString(message, 'after.date_join'), 2) AS date_join,
--     JSONExtractUInt(message, 'after.user_id') AS user_id
-- FROM _kafka_customers
-- SETTINGS stream_like_engine_allow_direct_select = 1;

-- ------------------------------ Bảng store
-- CREATE TABLE IF NOT EXISTS store (
--     id UInt32,
--     store_name LowCardinality(String),
--     date_join DateTime64(2)
-- )
-- ENGINE MergeTree
-- ORDER BY (id);

-- CREATE TABLE IF NOT EXISTS _kafka_store (
--     `message` String
-- )
-- ENGINE Kafka
-- SETTINGS
--     kafka_broker_list = 'kafka-postgres:19092',
--     kafka_topic_list = 'postgresDB.public.vendors',
--     kafka_group_name = 'clickhouse_store_consumer',
--     kafka_format = 'JSONAsString',
--     kafka_num_consumers = 1,
--     kafka_max_block_size = 1048576;

-- CREATE MATERIALIZED VIEW IF NOT EXISTS mv_store TO store AS
-- SELECT
--     JSONExtractUInt(message, 'after.id') AS id,
--     JSONExtractString(message, 'after.name') AS store_name,
--     parseDateTime64BestEffort(JSONExtractString(message, 'after.date_join'), 2) AS date_join
-- FROM _kafka_store
-- SETTINGS stream_like_engine_allow_direct_select = 1;

-- -------------------------- Bảng users
-- CREATE TABLE IF NOT EXISTS users (
--     id UInt32,
--     is_customer Boolean,
--     is_store Boolean,
--     address_id UInt32,
--     ttl DateTime DEFAULT now()
-- )
-- ENGINE MergeTree
-- ORDER BY (id)
-- TTL ttl + INTERVAL 1 DAY;

-- -- Bảng Kafka
-- CREATE TABLE IF NOT EXISTS _kafka_users (
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

-- CREATE MATERIALIZED VIEW IF NOT EXISTS mv_users TO users AS
-- SELECT
--     JSONExtractUInt(message, 'after.id') AS id,
--     JSONExtractBool(message, 'after.is_customer') AS is_customer,
--     JSONExtractBool(message, 'after.is_vendor') AS is_store,
--     JSONExtractUInt(message, 'after.address_id') AS address_id
-- FROM _kafka_users
-- SETTINGS stream_like_engine_allow_direct_select = 1;

-- ------------------------------ Tạo bảng dim_customer
-- CREATE TABLE IF NOT EXISTS dim_customer (
--     id UInt32,
--     fullname LowCardinality(String),
--     gender LowCardinality(String),
--     date_of_birth DateTime64(2),
--     date_join DateTime64(2),
--     ttl DateTime DEFAULT now()
-- )
-- ENGINE = MergeTree
-- ORDER BY (id)
-- TTL ttl + INTERVAL 1 DAY;

-- -- Materialized View để tạo dim_customer bằng cách join customers và users
-- CREATE MATERIALIZED VIEW IF NOT EXISTS mv_dim_customer TO dim_customer AS
-- SELECT
--     c.id AS id,
--     c.fullname AS fullname,
--     c.gender AS gender
--     c.date_of_birth AS date_of_birth,
--     c.date_join AS date_join
-- FROM customers AS c
-- SETTINGS stream_like_engine_allow_direct_select = 1;

------------------------------ reviews table
CREATE TABLE IF NOT EXISTS reviews (
    review_id UInt32,
    review_content LowCardinality(String),
    review_rating UInt32,
    review_date Datetime64(2),
    customer_id_id UInt32,
    product_id_id UInt32,
    ttl DateTime DEFAULT now()
)
ENGINE MergeTree
ORDER BY (review_id)
PARTITION BY toYYYYMM(review_date)
TTL ttl + INTERVAL 1 DAY;

CREATE TABLE IF NOT EXISTS _kafka_reviews (
    `message` String
)
ENGINE Kafka
SETTINGS
    kafka_broker_list = 'kafka-postgres:19092',
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
    parseDateTime64BestEffort(JSONExtractString(message, 'after.review_date'), 2) AS review_date,
    JSONExtractUInt(message, 'after.customer_id_id') AS customer_id_id,
    JSONExtractUInt(message, 'after.product_id_id') AS product_id_id
FROM _kafka_reviews
SETTINGS stream_like_engine_allow_direct_select = 1;
