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
GROUP BY 
    d.year, d.month
ORDER BY 
    d.year, d.month

