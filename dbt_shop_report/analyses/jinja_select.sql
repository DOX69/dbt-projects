{%set cols_list = ["sales_id","product_sk","discount_amount"]%}

SELECT
    {% for col in cols_list %}
        {{-col}}{%if not loop.last%}, {%endif%}
    {% endfor %}
FROM {{ ref('fact_sales_product_enriched') }}