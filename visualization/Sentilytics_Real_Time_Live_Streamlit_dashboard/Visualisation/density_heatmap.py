import streamlit as st
import pandas as pd
import plotly.express as px
from utils import get_hive_connection

def compare_platforms_component(start_date, end_date, sentiment):
    query = f"""
    SELECT published_date, sentiment, count
    FROM  comments_sentiment_by_date
    WHERE published_date BETWEEN '{start_date}' AND '{end_date}'
    """
    if sentiment != "all":
        query += f" AND sentiment = '{sentiment}'"
    query += " ORDER BY published_date"

    # Exécuter la requête Hive
    conn = get_hive_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # Organiser les données dans un DataFrame
        all_dates = []
        sentiment_types = ['positive', 'negative', 'neutral']
        data = []

        for row in results:
            date = row[0]
            sentiment_type = row[1]
            count = row[2]
            all_dates.append(date)
            data.append([date, sentiment_type, count])

        # Convertir en DataFrame
        df = pd.DataFrame(data, columns=['date', 'sentiment', 'count'])

        # Créer le graphique de type density_heatmap
        fig = px.density_heatmap(df, 
                                 x='date', 
                                 y='sentiment', 
                                 z='count', 
                                 color_continuous_scale='Viridis', 
                                 labels={"date": "Date", "sentiment": "Sentiment", "count": "Densité"})

        # Afficher le graphique
        st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Erreur lors de l'exécution de la requête : {e}")
    finally:
        if conn:
            conn.close()
