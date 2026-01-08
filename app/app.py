"""
app/app.py
==========
Dashboard Streamlit avec données réelles depuis Databricks.
Démontre : connexion sécurisée, caching, transformations, visualisations.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import logging
from datetime import datetime

from utils_databricks import (
    get_databricks_connection,
    load_agg_sales,
    get_sales_summary
)

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================================
# Page config
# ================================
st.set_page_config(
    page_title="Sales Analytics | Databricks",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ================================
# Titre
# ================================
st.title("📊 Sales Analytics Dashboard")
st.markdown(
    """
    **Données RÉELLES depuis Databricks** | Pipeline dbt complet.
    
    Architecture:
    - **Source** : Databricks SQL tables (Gold layer)
    - **App** : Streamlit + Python
    - **Sécurité** : Secrets management (PAT token chiffré)
    - **Caching** : Optimisé pour perfs
    """
)

# ================================
# Chargement des données
# ================================
try:
    with st.spinner("Chargement des données Databricks..."):
        df_agg_sales = load_agg_sales()
    
    st.success("✅ Données chargées avec succès !")

except Exception as e:
    st.error(f"❌ Erreur lors du chargement : {str(e)}")
    st.info(
        """
        **Vérifications :**
        - ✓ Token Databricks configuré dans `.streamlit/secrets.toml` ?
        - ✓ Host/HTTP path corrects ?
        - ✓ Permissions sur les tables gold ?
        - ✓ Tables existent : `main.gold.fact_sales`, etc ?
        """
    )
    st.stop()

# ================================
# Sidebar : Filtres
# ================================
st.sidebar.header("🎚️ Filtres & Contrôles")

# Conversion initiale
df_agg_sales["sales_date"] = pd.to_datetime(df_agg_sales["sales_date"])
df_agg_sales["sales_date"] = df_agg_sales["sales_date"].dt.date

# Filtre date
date_min = df_agg_sales["sales_date"].min()
date_max = df_agg_sales["sales_date"].max()

# Widgets
start_date = st.sidebar.date_input("Date de début", value=date_min, min_value=date_min, max_value=date_max)
end_date = st.sidebar.date_input("Date de fin", value=date_max, min_value=date_min, max_value=date_max)

# Filtre produit
all_products = ["Tous"] + sorted(df_agg_sales["product_name"].unique().tolist())
selected_product = st.sidebar.multiselect(
    "Filtrer par produit",
    options=all_products,
    default=["Tous"],
)

# Filtre country
all_countries = ["Tous"] + sorted(df_agg_sales["country"].unique().tolist())
selected_country = st.sidebar.multiselect(
    "Filtrer par pays",
    options=all_countries,
    default=["Tous"],
)

st.sidebar.markdown("---")
st.sidebar.info(
    """
    📌 **Infos:**
    - Données en temps quasi-réel (cache 5 min)
    - Tables : Gold layer (dbt)
    - Pipeline : Databricks SQL
    """
)

# ================================
# Appliquer filtres
# ================================
df_filtered = df_agg_sales.copy()

# Date
df_filtered = df_filtered[
    (df_filtered["sales_date"] >= start_date)
    & (df_filtered["sales_date"] <= end_date)
]

# Produit
if selected_product != ["Tous"]:
    df_filtered = df_filtered[
        df_filtered["product_name"].isin(selected_product)
    ]

# Country
if selected_country != ["Tous"]:
    df_filtered = df_filtered[
        df_filtered["country"].isin(
            df_agg_sales[df_agg_sales["country"].isin(selected_country)]["country"]
        )
    ]
# ================================
# KPIs
# ================================
summary = get_sales_summary(df_filtered)

st.subheader("📌 KPIs Principaux")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "💰 Chiffre d'affaires",
        f"€ {summary['total_revenue']:,.2f}",
    )
with kpi2:
    st.metric(
        "📦 Quantité vendue",
        f"{int(summary['total_quantity']):,}",
    )
with kpi3:
    st.metric(
        "🛒 Panier moyen",
        f"€ {summary['avg_ticket']:,.2f}",
    )
with kpi4:
    st.metric(
        "🧮 Transactions",
        f"{int(summary['total_transactions']):,}",
    )

st.markdown("---")

# ================================
# Graphiques
# ================================
st.subheader("📈 Analyses détaillées")

tab1, tab2, tab3 = st.tabs(["Journalier","Par jour de la semaine","Données"])

with tab1:
    col_rev, col_qty = st.columns(2)
    
    with col_rev:
        daily_amount = df_filtered.groupby(["sales_date",'country']).agg(
            total_gross_amount=("total_gross_amount", "sum")).reset_index()
        fig = px.bar(
            daily_amount,
            x="sales_date",
            y="total_gross_amount",
            color="country",
            title="Revenu brut par jour par pays",
        )
        fig.update_layout(template="plotly_white", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_qty:
        daily_quantity = df_filtered.groupby(["sales_date",'country']).agg(
            quantity=("quantity", "sum")).reset_index()
        fig = px.bar(
            daily_quantity,
            x="sales_date",
            y="quantity",
            title="Quantité par jour",
            color="country",
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
with tab2:
    st.subheader("Revenu brut par jour de la semaine")
    daily_quantity = df_filtered.groupby(["french_day_of_week_name",'country']).agg(
        total_gross_amount=("total_gross_amount", "sum")).reset_index()
    fig = px.bar(
        daily_quantity,
        x="french_day_of_week_name",
        y="total_gross_amount",
        title="Revenu brut par jour",
        color="country",
    )
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Données brutes filtrées")
    df_display = df_filtered
    st.dataframe(
        df_display.sort_values("sales_date", ascending=False),
        use_container_width=True,
        height=400,
    )

# ================================
# Footer
# ================================
st.markdown("---")
st.markdown(
    f"""
    <small>
      
    📅 **last update** : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
    
    📚 **Liens** :
    [GitHub: dbt-projects](https://github.com/DOX69/dbt-projects) 
    | [dbt Docs](https://dox69.github.io/dbt-projects)
    
    ⚙️ **Stack** : Databricks + SQL + dbt + Streamlit
    </small>
    """,
    unsafe_allow_html=True,
)
