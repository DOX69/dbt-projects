SELECT 
*
FROM 
    {{ ref('fact_sales_product_enriched') }}
WHERE
    net_amount IS NULL OR net_amount < 0