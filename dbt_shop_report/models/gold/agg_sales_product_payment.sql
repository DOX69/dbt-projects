SELECT 
    payment_method,
    product_name,
    round(SUM(net_amount),2) AS total_sales_net_amount
FROM 
    {{ source('silver', 'fact_sales_product_enriched') }}
GROUP BY ROLLUP (
    payment_method,
    product_name)