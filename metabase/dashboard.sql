-- Doanh Số Theo Danh Mục Sản Phẩm
SELECT
    p.category,
    SUM(f.total_amount) AS total_sales
FROM
    fact_sales f
JOIN
    dim_product p ON f.product_id = p.id
WHERE
    f.shop_id = {{shop_id}}
GROUP BY
    p.category
ORDER BY
    total_sales DESC

-- Doanh Số Theo Giới Tính Khách Hàng
SELECT
    c.gender,
    SUM(f.total_amount) AS total_sales
FROM
    fact_sales f
JOIN
    dim_customer c ON f.customer_id = c.id
WHERE
    f.shop_id = {{shop_id}}
GROUP BY
    c.gender
ORDER BY
    total_sales DESC

-- Doanh thu theo tháng
SELECT 
    d.year,
    d.month,
    SUM(f.total_amount) AS total_sales
FROM 
    fact_sales f
JOIN 
    dim_date d ON f.date_id = d.id
WHERE 
    f.status = 'completed'
    AND f.shop_id = {{shop_id}}
GROUP BY 
    d.year, d.month
ORDER BY 
    d.year, d.month

-- Hiệu Quả Các Chương Trình Khuyến Mãi
SELECT
    pr.name AS promotion_name,
    COUNT(f.id) AS number_of_sales,
    SUM(f.total_amount) AS total_sales
FROM
    fact_sales f
JOIN
    dim_promotion pr ON f.promotion_id = pr.id
WHERE
    f.shop_id = {{shop_id}} AND
    f.promotion_id IS NOT NULL
GROUP BY
    pr.name
ORDER BY
    total_sales DESC

-- Phân Tích Khách Hàng
SELECT
    c.gender,
    COUNT(c.id) AS number_of_customers
FROM
    dim_customer c
JOIN
    fact_sales f ON c.id = f.customer_id
WHERE
    f.shop_id = {{shop_id}}
GROUP BY
    c.gender

-- Sản phẩm bán chạy
SELECT 
    p.name AS product_name,
    SUM(f.quantity) AS total_quantity_sold,
    SUM(f.total_amount) AS total_sales
FROM 
    fact_sales f
JOIN 
    dim_product p ON f.product_id = p.id
WHERE 1=1
    AND f.shop_id = {{shop_id}}
GROUP BY 
    p.name
ORDER BY 
    total_sales DESC
limit 5;

-- Số Lượng Khách Hàng Mới
SELECT
    COUNT(DISTINCT c.id) AS new_customers
FROM
    dim_customer c
JOIN
    fact_sales f ON c.id = f.customer_id
WHERE
    f.shop_id = {{shop_id}}

-- Số Lượng Review
SELECT
    COUNT(r.id) AS total_reviews
FROM
    fact_review r
JOIN
    dim_store s ON r.shop_id = s.id
WHERE
    r.shop_id = {{shop_id}}
GROUP BY
    s.store_name

-- Số lượng đơn hàng
select count(*)
from fact_sales f
where f.shop_id = {{shop_id}};

-- Top 10 Review Rating Cao Nhất
SELECT
    c.fullname AS customer_name,
    p.name AS product_name,
    r.content AS review_content,
    r.rating AS review_rating,
    r.date_post AS review_date
FROM
    fact_review r
JOIN
    dim_customer c ON r.customer_id = c.id
JOIN
    dim_product p ON r.product_id = p.id
WHERE
    r.shop_id = {{shop_id}}
ORDER BY
    r.rating DESC
LIMIT 10

-- Trung Bình Rating Của Cửa Hàng
SELECT
    AVG(r.rating) AS average_rating
FROM
    fact_review r
JOIN
    dim_store s ON r.shop_id = s.id
WHERE
    r.shop_id = {{shop_id}}
GROUP BY
    s.store_name

-- Tổng Doanh Thu So Với Mục Tiêu
SELECT sum(`total_amount`) AS `SUM(total_amount)_002f96`
FROM `default`.`fact_sales`
WHERE 1=1
    and`status` ='completed' 
    AND `shop_id` = {{shop_id}};
    
--------------------------------------------------------------
-- Doanh Số Theo Danh Mục Sản Phẩm
SELECT
    p.category,
    SUM(f.total_amount) AS total_sales
FROM
    fact_sales f
JOIN
    dim_product p ON f.product_id = p.id
WHERE
    f.shop_id = {{shop_id}}
GROUP BY
    p.category
ORDER BY
    total_sales DESC

-- Doanh Số Theo Giới Tính Khách Hàng
SELECT
    c.gender,
    SUM(f.total_amount) AS total_sales
FROM
    fact_sales f
JOIN
    dim_customer c ON f.customer_id = c.id
WHERE
    f.shop_id = {{shop_id}}
GROUP BY
    c.gender
ORDER BY
    total_sales DESC;

-- Doanh Thu Theo Tháng
SELECT 
    d.year,
    d.month,
    SUM(f.total_amount) AS total_sales
FROM 
    fact_sales f
JOIN 
    dim_date d ON f.date_id = d.id
WHERE 
    f.status = 'completed'
    AND f.shop_id = {{shop_id}}
    AND d.year = {{year}}
GROUP BY 
    d.year, d.month
ORDER BY 
    d.year, d.month;

-- Số Lượng Giao Dịch
SELECT 
    COUNT(fs.id) AS "Số Lượng Giao Dịch"
FROM
    fact_sales fs
JOIN
    dim_store ds ON fs.shop_id = ds.id
WHERE
    fs.shop_id = {{shop_id}}
GROUP BY
    ds.store_name
ORDER BY
    "Số Lượng Giao Dịch" DESC;

-- Trung Bình Rating Của Cửa Hàng
SELECT
    AVG(r.rating) AS average_rating
FROM
    fact_review r
JOIN
    dim_store s ON r.shop_id = s.id
WHERE
    r.shop_id = {{shop_id}}
GROUP BY
    s.store_name;

-- Tổng Doanh Thu
SELECT sum(`total_amount`) AS `SUM(total_amount)_002f96` FROM `default`.`fact_sales` WHERE `status` ='completed' AND `shop_id` = {{shop_id}};

-- Tổng Doanh Thu So Với Mục Tiêu
SELECT sum(`total_amount`) AS `total_amount`
FROM `default`.`fact_sales`
WHERE
    `status` ='completed' 
    AND `shop_id` = {{shop_id}};