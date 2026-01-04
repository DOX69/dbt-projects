WITH multiply AS (
    SELECT round({{ multiply('unit_price', 'quantity') }},2) AS calculated_gross_amount,
           gross_amount,
           sales_id,
           unit_price,
           quantity
    FROM {{source('bronze','csv_fact_sales')}}
)
SELECT *
FROM multiply
WHERE round(gross_amount, 2) != calculated_gross_amount