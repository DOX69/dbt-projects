{%set is_incremental = True%}
{% set last_load_sk = 3%}

SELECT *
FROM {{ ref("fact_sales_product_enriched") }}
{% if is_incremental %}
WHERE sales_sk > {{ last_load_sk }}
{% endif %}