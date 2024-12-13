use default;

CREATE TABLE category (
    id Int32,
    name String,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id;

CREATE TABLE user_address (
    user_id Int32,
    address_id Int32
) ENGINE = MergeTree()
ORDER BY user_id;

CREATE TABLE dim_date (
    id Int32,
    full_date Date,
    day Int32,
    month Int32,
    year Int32,
    quarter Int32,
    day_of_week String,
    week_of_month Int32,
    holiday String,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id
PARTITION BY toYYYYMM(full_date)
SETTINGS index_granularity = 8192;

CREATE TABLE dim_customer (
    id Int32,
    full_name String,
    gender String,
    date_of_birth Datetime64,
    date_join Datetime64,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id
SETTINGS index_granularity = 8192;

CREATE TABLE dim_store (
    id Int32,
    store_name String,
    date_join Datetime64,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id
SETTINGS index_granularity = 8192;

-- CREATE TABLE dim_promotion (
--     id Int32,
--     name String,
--     discount_rate Float32,
--     PRIMARY KEY (id)
-- ) ENGINE = MergeTree()
-- ORDER BY id
-- SETTINGS index_granularity = 8192;

CREATE TABLE dim_product (
    id Int32,
    name String,
    brand String,
    price Float32,
    stock Int32,
    category String,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id
SETTINGS index_granularity = 8192;

CREATE TABLE dim_province (
    id Int32,
    province_name String,
    is_city Boolean,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id
SETTINGS index_granularity = 8192;

CREATE TABLE fact_sales (
    id Int32,
    quantity Int32,
    total_price Float32,
    total_amount Float32,
    status Boolean,
    date_id Int32,
    product_id Int32,
    customer_id Int32,
    store_id Int32,
    location_id Int32,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
PARTITION BY store_id
ORDER BY (date_id, id)
-- partition by store_id


SETTINGS index_granularity = 8192;

CREATE TABLE fact_review (
    id Int32,
    content String,
    rating Int32,
    date_id Int32,
    product_id Int32,
    customer_id Int32,
    store_id Int32,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY (date_id, id)
PARTITION BY store_id
SETTINGS index_granularity = 8192;