import pandas as pd
import plotly.express as px
import streamlit as st
from utils import get_hive_connection

def counts(start_date, end_date, sentiment):
    # Connexion à Hive
    conn = get_hive_connection()

    try:
        # Requête Hive pour obtenir la distribution des sentiments
        query = f"""
        SELECT prediction, SUM(count) AS count 
        FROM  comments_sentiment_distribution
        WHERE published_date BETWEEN '{start_date}' AND '{end_date}'
        """
        if sentiment != "all":
            query += f" AND prediction = '{sentiment}'"
        query += " GROUP BY prediction"


        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # Convertir les résultats en DataFrame
        df = pd.DataFrame(results, columns=["prediction", "count"])

        # Vérifier si des données sont disponibles
        if df.empty:
            st.warning("Aucune donnée trouvée pour cette période et ce sentiment.")
        else:

           
            # Associer chaque sentiment à son count
            negative_count = df.loc[df['prediction'] == 'negative', 'count'].values[0] if not df.loc[df['prediction'] == 'negative'].empty else 0
            neutral_count = df.loc[df['prediction'] == 'neutral', 'count'].values[0] if not df.loc[df['prediction'] == 'neutral'].empty else 0
            positive_count = df.loc[df['prediction'] == 'positive', 'count'].values[0] if not df.loc[df['prediction'] == 'positive'].empty else 0

            # Utilisation des colonnes Streamlit pour afficher les résultats
            kpi1, kpi2, kpi3 = st.columns(3)

            # Remplir les trois colonnes avec les valeurs correspondantes
            kpi1.metric(label="Negative 🤬", value=negative_count)
            kpi2.metric(label="Neutral 😑", value=neutral_count)
            kpi3.metric(label="Positive 💕", value=positive_count)
    except Exception as e:
        st.error(f"Erreur lors de l'exécution de la requête : {e}")
    finally:
        if conn: 
            conn.close()
