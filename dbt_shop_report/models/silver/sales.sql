{{config(
    materialized='table',
    database='dev',
    schema='sales'
)}}

SELECT
fs.* except(load_timestamp,source_file),
dp.* except(load_timestamp,source_file,product_sk)
FROM
{{source('table_sources', 'csv_fact_sales')}} as fs
LEFT JOIN
{{source('table_sources', 'csv_dim_product')}} as dp
using(product_sk)