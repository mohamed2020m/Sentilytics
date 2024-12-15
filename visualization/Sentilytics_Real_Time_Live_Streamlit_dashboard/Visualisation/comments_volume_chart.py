import pandas as pd
import plotly.express as px
import streamlit as st
from utils import get_hive_connection

def generate_comments_volume_chart(start_date, end_date, sentiment):
    # Connexion à Hive
    conn = get_hive_connection()

    try:
        # Requête Hive pour obtenir le volume de commentaires par source et sentiment dans la période spécifiée
        query = f"""
        SELECT source, prediction, SUM(count) AS count 
        FROM comments_volume_by_sentiment
        WHERE published_date BETWEEN '{start_date}' AND '{end_date}'
        """
        if sentiment != "all":
            query += f" AND prediction = '{sentiment}'"
        query += " GROUP BY source, prediction"


        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # Convertir les résultats en DataFrame
        df = pd.DataFrame(results, columns=["source", "prediction", "count"])

        # Vérifier si des données sont disponibles
        if df.empty:
            st.warning("Aucune donnée trouvée pour cette période et ce sentiment.")
        else:
            # Assurer que toutes les catégories de sentiments (positive, negative, neutral) sont présentes
            # pour chaque source, même si elles sont absentes dans certaines lignes.
            all_sentiments = ["positive", "negative", "neutral"]

            # Pivot du DataFrame pour avoir une colonne par sentiment
            df_pivot = df.pivot_table(index="source", columns="prediction", values="count", aggfunc="sum", fill_value=0)

            # Ajouter les colonnes manquantes si elles n'existent pas déjà
            for sentiment in all_sentiments:
                if sentiment not in df_pivot.columns:
                    df_pivot[sentiment] = 0

            # Réorganiser les colonnes pour être dans l'ordre voulu
            df_pivot = df_pivot[all_sentiments]

            # Générer le Stacked Bar Chart
            fig = px.bar(df_pivot, x=df_pivot.index, y=all_sentiments,
                         labels={"value": "Nombre de Commentaires", "source": "Source"})
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Erreur lors de l'exécution de la requête : {e}")
    finally:
        if conn: 
            conn.close()
