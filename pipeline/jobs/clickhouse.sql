-- Bảng Dimension: dim_province
CREATE TABLE dim_province (
    id UInt32,
    province_name String,
    is_city UInt8,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id;

-- Bảng Dimension: dim_date
CREATE TABLE dim_date (
    id UInt32,
    full_date Date,
    day UInt8,
    month UInt8,
    year UInt16,
    quarter UInt8,
    day_of_week UInt8,
    week_of_year UInt8,
    is_weekend Boolean,
    is_holiday String,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(full_date)
ORDER BY id;

-- Bảng Dimension: dim_customer
CREATE TABLE dim_customer (
    id UInt32,
    fullname String,
    gender String,
    date_of_birth DateTime,
    date_join DateTime,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id;

-- Bảng Dimension: dim_store
CREATE TABLE dim_store (
    id UInt32,
    store_name String,
    date_join DateTime,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id;

-- Bảng Dimension: dim_promotion
CREATE TABLE dim_promotion (
    id UInt32,
    name String,
    discount_rate Float32,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id;

-- Bảng Dimension: dim_product
CREATE TABLE dim_product (
    id UInt32,
    name String,
    brand String,
    price Float64,
    stock Int32,
    category String,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
ORDER BY id;

-- Bảng Fact: fact_sales
CREATE TABLE fact_sales (
    id UInt32,
    quantity Int32,
    total_amount Float64,
    status String,
    date_id UInt32,
    promotion_id Nullable(UInt32),
    location_id UInt32,
    product_id UInt32,
    customer_id UInt32,
    shop_id UInt32,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
PARTITION BY (shop_id)
ORDER BY id;

-- Bảng Fact: fact_review
CREATE TABLE fact_review (
    id UInt32,
    content String,
    rating Int32,
    date_post DateTime,
    product_id UInt32,
    customer_id UInt32,
    shop_id UInt32,
    PRIMARY KEY (id)
) ENGINE = MergeTree()
PARTITION BY (shop_id)
ORDER BY id;