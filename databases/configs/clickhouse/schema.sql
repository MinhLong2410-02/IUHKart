use default;

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
    first_name String,
    middle_name String,
    last_name String,
    gender String,
    date_of_birth Date,
    signup_date Date,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id
SETTINGS index_granularity = 8192;

CREATE TABLE dim_store (
    id Int32,
    shop_name String,
    establish_date Date,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id
SETTINGS index_granularity = 8192;

CREATE TABLE dim_promotion (
    id Int32,
    name String,
    discount_rate Float32,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id
SETTINGS index_granularity = 8192;

CREATE TABLE dim_product (
    id Int32,
    name String,
    brand String,
    price Float32,      -- Đổi từ VARCHAR sang FLOAT để phù hợp với giá
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
    promotion_id Int32,
    customer_id Int32,
    shop_id Int32,
    location_id Int32
) ENGINE = MergeTree()
ORDER BY (date_id, id)
SETTINGS index_granularity = 8192;

CREATE TABLE fact_review (
    id Int32,
    content String,
    rating Int32,
    sentiment_score Int32,
    date_id Int32,
    product_id Int32,
    customer_id Int32,
    store_id Int32
) ENGINE = MergeTree()
ORDER BY (date_id, id)
SETTINGS index_granularity = 8192;
