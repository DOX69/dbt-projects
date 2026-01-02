SELECT 
*
FROM 
    {{ ref('sales') }}
WHERE
    net_amount IS NULL OR net_amount < 0