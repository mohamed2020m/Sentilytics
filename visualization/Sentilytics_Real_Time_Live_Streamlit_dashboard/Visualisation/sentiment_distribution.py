import pandas as pd
import plotly.express as px
import streamlit as st
from utils import get_hive_connection

def display_sentiment_distribution(start_date, end_date, sentiment):
    # Connexion à Hive
    conn = get_hive_connection()

    try:
        # Requête Hive pour obtenir la distribution des sentiments
        query = f"""
        SELECT prediction, COUNT(*) AS count 
        FROM belkdb.comments 
        WHERE publishedAt BETWEEN '{start_date}' AND '{end_date}'
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
            
            st.subheader("Volume des Commentaires par Source")
            col1, col2 = st.columns([1, 2])  

            with col1:
                sentiment_counts = df.set_index("prediction")["count"]
                st.bar_chart(sentiment_counts)

            with col2:
                fig = px.pie(df, names='prediction', values='count')
                st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Erreur lors de l'exécution de la requête : {e}")
    finally:
        if conn: 
            conn.close()
