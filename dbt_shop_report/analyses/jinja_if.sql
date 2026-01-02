{%- set payment_method = ["Card", "Cash", "Credit", "E-wallet"] -%}
{%- if "E-wallet" in payment_method -%}
    E-wallet is available as a payment method.
{%- else -%}
    E-wallet is not available as a payment method.
{%- endif -%}