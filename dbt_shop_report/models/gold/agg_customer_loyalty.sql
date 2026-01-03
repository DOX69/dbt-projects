SELECT
       customer_code,
       loyalty_tier,
       COUNT(sales_id) AS total_purchases,
       COUNT(CASE WHEN is_promoted THEN sales_id END) AS total_promoted_purchases,
       ROUND(SUM(gross_amount),2) AS total_gross_amount,
       ROUND(SUM(discount_amount),2) AS total_discount_amount,
       ROUND(SUM(net_amount),2) AS total_net_amount
FROM
{{ ref('fact_customer_sales_enriched') }}
GROUP BY 
    customer_code,
    loyalty_tier