{% set payment_method = ["Card", "Cash", "Credit", "E-wallet"] %} 
{% for method in payment_method %}
    {{ method }}
{% endfor %}