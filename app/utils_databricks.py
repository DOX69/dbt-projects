"""
app/utils_databricks.py
======================
Gestion de la connexion Databricks et chargement des données.
Utilise st.secrets pour la sécurité.
"""

import streamlit as st
import pandas as pd
from databricks import sql
from databricks.sql.client import Connection 
from typing import Optional
import logging

# Configuration du logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO) 


@st.cache_resource
def get_databricks_connection() -> Connection: 
    """
    Crée une connexion Databricks réutilisable.
    
    Lecture depuis st.secrets (local ou Streamlit Cloud).
    Utilise le decorator @cache_resource pour une seule connexion par session.
    
    Returns:
        sql.Connection: Connexion Databricks active
        
    Raises:
        KeyError: Si les credentials manquent dans st.secrets
        Exception: Si la connexion échoue
    """
    try:
        # 1️⃣ Récupérer les credentials depuis st.secrets
        host = st.secrets["databricks"]["host"]
        token = st.secrets["databricks"]["token"]
        http_path = st.secrets["databricks"]["http_path"]
        
        # 2️⃣ Créer la connexion (API MODERNE)
        conn = sql.connect(
            server_hostname=host,
            http_path=http_path,
            access_token=token 
        )
        
        logger.info("✅ Connexion Databricks établie avec succès")
        return conn
    except KeyError as e:
        st.error(f"❌ Clé manquante dans secrets: {e}")
        st.info("Ajoute tes credentials...")
        logger.error(f"KeyError: {e}")  # ✅ Log l'erreur
        raise

    except Exception as e:
        st.error(f"❌ Erreur de connexion Databricks: {e}")
        logger.error(f"Connection Error: {e}", exc_info=True)  # ✅ Full traceback
        raise

@st.cache_data(ttl=300)  # Cache 5 min
def load_agg_sales(limit: Optional[int] = None) -> pd.DataFrame:
    """
    Charge la table agg_sales depuis Databricks Gold layer.
    
    Args:
        limit: nombre max de lignes (None = tout)
    
    Returns:
        DataFrame avec sales transactions
    """
    conn = get_databricks_connection()
    
    query = """
    WITH AGG AS (
    SELECT
        date as sales_date,
        sales.product_name,
        store.country,
        CASE date_format(date, 'EEEE')
            WHEN 'Monday' THEN '1- Lundi'
            WHEN 'Tuesday' THEN '2- Mardi'
            WHEN 'Wednesday' THEN '3- Mercredi'
            WHEN 'Thursday' THEN '4- Jeudi'
            WHEN 'Friday' THEN '5- Vendredi'
            WHEN 'Saturday' THEN '6- Samedi'
            WHEN 'Sunday' THEN '7- Dimanche'
        ELSE date_format(date, 'EEEE')
        END as french_day_of_week_name,
        sum(quantity) quantity,
        count(distinct sales.sales_id) as num_transactions,
        round(sum(sales.gross_amount), 0) as total_gross_amount
    FROM
        prod.silver.fact_sales_product_enriched AS sales
        LEFT JOIN prod.bronze.csv_dim_date as date USING (date_sk)
        LEFT JOIN prod.bronze.csv_dim_store as store USING (store_sk)
    GROUP BY
        ALL
    )
    SELECT
    *,
    round(sum(total_gross_amount) over () / sum(num_transactions) over (), 0) as avg_ticket
    FROM
    AGG
    ORDER BY
    sales_date DESC
    """
    
    if limit:
        query += f" LIMIT {limit}"
    
    df = pd.read_sql(query, conn)

    logger.info(f"✅ Chargé {len(df)} lignes de agg_sales")
    return df

def get_sales_summary(df_sales: pd.DataFrame) -> dict:
    """Agrégations principales."""
    return {
        "total_revenue": df_sales["total_gross_amount"].sum(),
        "total_transactions": df_sales["num_transactions"].sum(),
        "total_quantity": df_sales["quantity"].sum(),
        "avg_ticket": df_sales["avg_ticket"].mean(),
        "date_min": df_sales["sales_date"].min(),
        "date_max": df_sales["sales_date"].max(),
    }