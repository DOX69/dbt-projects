SELECT sales_id,
gross_amount,
round((unit_price * quantity), 2) AS calculated_gross_amount,
unit_price,
quantity 
FROM {{source('bronze','csv_fact_sales')}}
WHERE round(gross_amount, 2) != round((unit_price * quantity), 2)