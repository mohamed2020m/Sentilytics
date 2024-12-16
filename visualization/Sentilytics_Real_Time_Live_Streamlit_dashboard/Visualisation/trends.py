# trends.py
import pandas as pd
import plotly.express as px
import streamlit as st
from utils import get_hive_connection

def generate_trends_chart(start_date, end_date, sentiment):
    # Connexion à Hive
    conn = get_hive_connection()

    try:
        # Requête Hive pour récupérer les commentaires par date et sentiment
        query = f"""
        SELECT published_date, sentiment, count
        FROM comments_trends
        WHERE published_date BETWEEN '{start_date}' AND '{end_date}'
        """
        if sentiment != "all":
            query += f" AND sentiment = '{sentiment}'"
        query += " ORDER BY published_date"


        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # Convertir les résultats en DataFrame
        df = pd.DataFrame(results, columns=["publishedAt", "prediction", "count"])

        # Vérifier si des données sont disponibles
        if df.empty:
            st.warning("No data found for this period and sentiment.")
        else:
            # Convertir la date en format datetime
            df['publishedAt'] = pd.to_datetime(df['publishedAt'])

            # Pivot du DataFrame pour avoir une colonne par sentiment
            df_pivot = df.pivot_table(index='publishedAt', columns='prediction', values='count', aggfunc='sum', fill_value=0)

            # Identifier les colonnes disponibles (sentiments présents)
            available_sentiments = ['positive', 'negative', 'neutral']
            present_sentiments = [sentiment for sentiment in available_sentiments if sentiment in df_pivot.columns]

            # Créer le Line Chart uniquement pour les sentiments disponibles
            st.subheader("Evolution of Comments Over Time")
            fig = px.line(df_pivot, x=df_pivot.index, y=present_sentiments,
                          labels={"value": "Number of Comments", "publishedAt": "Date", "prediction": "Sentiment"})
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error executing the query: {e}")
    finally:
        if conn: 
            conn.close()



