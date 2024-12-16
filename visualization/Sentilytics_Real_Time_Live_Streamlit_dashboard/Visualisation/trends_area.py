import streamlit as st
import pandas as pd
from utils import get_hive_connection

def generate_trends_area_chart(start_date, end_date, sentiment):
    # Construire la requête pour récupérer les sentiments par date
    sentiment_filter = f"AND prediction = '{sentiment}'" if sentiment != 'all' else ""
    query = f"""
    SELECT publishedAt, prediction, COUNT(*) as count
    FROM belkdb.comments 
    WHERE publishedAt BETWEEN '{start_date}' AND '{end_date}'
    {sentiment_filter}
    GROUP BY publishedAt, prediction
    ORDER BY publishedAt
    """
    
    # Exécuter la requête Hive
    conn = get_hive_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # Organiser les données dans un DataFrame
        data = {'date': [], 'positive': [], 'negative': [], 'neutral': []}

        # Remplir les dictionnaires avec des listes vides
        all_dates = set()
        for row in results:
            date = row[0]
            sentiment_type = row[1]
            count = row[2]
            all_dates.add(date)

            # Ajouter les données aux bonnes catégories
            if sentiment_type == 'positive':
                data['positive'].append((date, count))
            elif sentiment_type == 'negative':
                data['negative'].append((date, count))
            elif sentiment_type == 'neutral':
                data['neutral'].append((date, count))

        # Créer un DataFrame avec toutes les dates possibles
        all_dates = sorted(list(all_dates))
        
        # Dictionnaires pour chaque sentiment initialisé à zéro
        sentiment_data = {'positive': {}, 'negative': {}, 'neutral': {}}
        
        for sentiment_type in ['positive', 'negative', 'neutral']:
            # Initialiser les dates avec 0
            sentiment_data[sentiment_type] = {date: 0 for date in all_dates}
            
            # Remplir avec les données existantes
            for date, count in data[sentiment_type]:
                sentiment_data[sentiment_type][date] = count

        # Créer le DataFrame final en utilisant les dates comme index
        df = pd.DataFrame({sentiment: [sentiment_data[sentiment].get(date, 0) for date in all_dates] 
                           for sentiment in ['positive', 'negative', 'neutral']})
        df['date'] = all_dates

        # Créer le graphique de type area_chart
        st.area_chart(df, x="date", y=["positive", "negative", "neutral"])

    except Exception as e:
        st.error(f"Error executing the query. : {e}")
    finally:
        if conn:
            conn.close()
