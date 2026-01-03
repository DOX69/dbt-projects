WITH sales_amount as (
    SELECT sales_id,
    customer_sk,
    discount_amount,
    net_amount,
    gross_amount,
    payment_method,
    CASE WHEN promotion_sk is not null then True ELSE False END as is_promoted
    FROM {{ source('bronze','csv_fact_sales')}}
)
, customer_info as (
    SELECT customer_sk,
    first_name,
    last_name,
    customer_code,
    gender,
    loyalty_tier
    FROM {{ source('bronze','csv_dim_customer')}}
)
SELECT 
    * 
FROM customer_info LEFT JOIN sales_amount using(customer_sk)