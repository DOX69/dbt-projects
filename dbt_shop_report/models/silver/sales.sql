--block level model
{{config(
    database='prod',
    schema= 'silver'
)}}

SELECT
fs.* except(load_timestamp,source_file),
dp.* except(load_timestamp,source_file,product_sk)
FROM
{{source('bronze', 'csv_fact_sales')}} as fs
LEFT JOIN
{{source('bronze', 'csv_dim_product')}} as dp
using(product_sk)