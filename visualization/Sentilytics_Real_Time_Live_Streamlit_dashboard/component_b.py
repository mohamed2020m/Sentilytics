import streamlit as st
import pandas as pd
import time
import random


# Mapping des IDs de chaînes à leurs noms
mapping = {
    "UCtxD0x6AuNNqdXO9Wp5GHew": "cr7",
    "UCX6OQ3DkcsbYNE6H8uQQuVA": "MrBeast",
    "UCSHZKyawb77ixDdsGog4iWA": "lexfridman",
    "": ""
}

@st.cache_data
def load_data_from_url() -> pd.DataFrame:
    df = pd.read_csv("data.csv")
    return df

def replace_channel_ids(df: pd.DataFrame) -> pd.DataFrame:
    # Remplacer les IDs des chaînes par leurs noms en utilisant le mapping
    df['channel'] = df['channel'].map(mapping).fillna(df['channel'])
    return df

def component_b():
    st.title("Real-Time Predictions Display")

    # Charger les données
    data = load_data_from_url()
    data = replace_channel_ids(data)


    # Initialiser l'index de début dans l'état de session
    if 'start_index' not in st.session_state:
        st.session_state['start_index'] = 0

    # Initialiser les données du chart dans l'état de session
    if 'chart_data' not in st.session_state:
        st.session_state['chart_data'] = pd.DataFrame(columns=["x", "y"])

    # Taille d'une tranche de données
    chunk_size = random.randint(1, 10)

    # Déterminer la plage d'indices pour la tranche actuelle
    start_index = st.session_state['start_index']
    end_index = start_index + chunk_size

    # Extraire la tranche de données
    subset = data.iloc[start_index:end_index]

    

    # Ajouter de nouveaux points pour le graphique selon le nombre de prédictions
    for i in range(chunk_size):
        # Extraire la prédiction depuis le dataframe
        prediction_type = subset.iloc[i]['prediction']  # Assurez-vous que le nom de la colonne est 'prediction'
        
        # Déterminer la valeur de 'y' en fonction de la prédiction
        if prediction_type == 'negative':
            y_value = -1
        elif prediction_type == 'positive':
            y_value = 1
        else:
            y_value = 0

        # Ajouter ce point au dataframe existant dans l'état de session
        new_point = pd.DataFrame({
            "x": [end_index + i],  # L'index des données
            "y": [y_value]         # La valeur de la prédiction (1, 0, -1)
        })

        # Ajouter ce point au dataframe existant
        st.session_state['chart_data'] = pd.concat([st.session_state['chart_data'], new_point], ignore_index=True)

    # Afficher les données
    st.write("### New Prediction Received")
    st.dataframe(subset)

    # Tracer le graphique linéaire dynamique (Cardiogramme)
    chart_data = st.session_state['chart_data']
    
    # Afficher le graphique avec Streamlit (line_chart)
    st.line_chart(chart_data.set_index('x')['y'])

    # Ajouter une personnalisation de l'axe Y pour avoir 'positive', 'neutral', 'negative'
    st.write("### Y-Axis Label")
    st.write(f"-1 : Negative Sentiment, 0 :  Neutral Sentiment, 1 : Positive Sentiment")

    # Mettre à jour l'index pour la tranche suivante
    if end_index < len(data):
        st.session_state['start_index'] = end_index
    else:
        st.session_state['start_index'] = 0  

    # Attendre un délai avant de relancer
    sleep = random.randint(5, 10)
    time.sleep(sleep)
    st.rerun()
