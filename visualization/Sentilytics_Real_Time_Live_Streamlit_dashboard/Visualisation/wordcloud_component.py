import streamlit as st
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re
from utils import get_hive_connection

def wordcloud_component(start_date, end_date, sentiment):
    # Appliquer un filtre de sentiment si nécessaire
    sentiment_filter = f"AND sentiment = '{sentiment}'" if sentiment != 'all' else ""
    
    query = f"""
    SELECT comment 
    FROM comments_wordcloud 
    WHERE publishedAt BETWEEN '{start_date}' AND '{end_date}' 
    {sentiment_filter}
    """


    
    # Exécuter la requête Hive
    conn = get_hive_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        comments = [row[0] for row in results]
        st.subheader("Word Cloud")

        # Vérifier si des commentaires existent
        if comments:
            generate_wordcloud(comments)
        else:
            st.warning("No comments found for this period and sentiment")
    except Exception as e:
        st.error(f"Error executing the query: {e}")
    finally:
        if conn:
            conn.close()

def generate_wordcloud(sentiment_data):
    text = ' '.join(sentiment_data)
    text = re.sub(r'[^\w\s]', '', text)  # Retirer la ponctuation
    text = text.lower()  # Convertir tout en minuscule

    # Génération du nuage de mots
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Affichage du nuage de mots
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
