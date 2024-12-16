# top_comments.py
import pandas as pd
import streamlit as st
from utils import get_hive_connection

def generate_top_commented_likes(start_date, end_date, sentiment):
    # Connexion à Hive
    conn = get_hive_connection()

    try:
        # Requête Hive pour récupérer les commentaires YouTube triés par likeCount
        query = """
        SELECT comment, likes, published_date, sentiment
        FROM top_commented_youtube 
        """

        # Ajout de la condition sentiment si nécessaire
        if sentiment != "all":
            query += f" WHERE sentiment = '{sentiment}'"

        # Ajout de la clause ORDER BY et LIMIT
        query += """
        ORDER BY likes DESC
        LIMIT 5
        """

        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # Convertir les résultats en DataFrame
        df = pd.DataFrame(results, columns=['Comment', 'Number of Likes', 'Date', 'Sentiment'])

        # Vérifier si des données sont disponibles
        if df.empty:
            st.warning("No comments found on YouTube.")
        else:
            # Ajouter une colonne avec le texte abrégé si trop long
            df["Comment"] = df["Comment"].apply(lambda x: x[:100] + "..." if len(x) > 100 else x)

            # Afficher le tableau interactif
            st.subheader("Most Liked Comments (YouTube)")
            st.dataframe(df[['Comment', 'Number of Likes', 'Date', 'Sentiment']], use_container_width=True)

    except Exception as e:
        st.error(f"Error executing the query : {e}")
    finally:
        if conn: 
            conn.close()
