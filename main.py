"""
app/utils_databricks.py
======================
Gestion de la connexion Databricks et chargement des données.
Utilise st.secrets pour la sécurité.
"""

import streamlit as st
# import pandas as pd
from databricks import sql
from databricks.sql.client import Connection 
# from typing import Optional
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


if __name__ == '__main__':
    st.title("🔌 Test Connexion Databricks")
    
    if st.button("Tester la connexion", type="primary"):
        with st.spinner("Vérification en cours..."):
            if get_databricks_connection():
                st.success("✅ Connexion établie!")
            else:
                st.error("❌ Impossible de se connecter")

