import streamlit as st
from sidebar import sidebar_button
from component_a import component_a
from component_b import component_b
from main_component import main_component

# Initialiser la configuration de la page une seule fois
st.set_page_config(
    page_title='Sentiment Analysis',
    page_icon='😊', 
    layout='wide'
)

# Fonction pour afficher un bouton personnalisé dans la sidebar
def custom_sidebar_button(label, icon, page_name):

    
    if st.sidebar.button(f"{icon} {label}"):
        st.session_state.page = page_name

def main():
    
    # Initialiser la page si pas déjà fait
    if 'page' not in st.session_state:
        st.session_state.page = "Accueil"
    
    # Sidebar personnalisée
    with st.sidebar:
        # Logo en haut de la sidebar
        st.image("image.png", width=250) 

        # Titre de la sidebar
        #st.markdown("### Analyse de Sentiment")

        # Espacement pour une meilleure lisibilité
        st.markdown("<br>", unsafe_allow_html=True)

        # Boutons pour naviguer entre les composants
        custom_sidebar_button("Home Page", "🏠", "Accueil")
        custom_sidebar_button("Historical Data", "🔍", "Composant A")
        custom_sidebar_button("Live Data Dashboard", "📊", "Composant B")
       

    # Contenu principal
    if st.session_state.page == "Composant A":
        component_a()
    elif st.session_state.page == "Composant B":
        component_b()
    elif st.session_state.page == "Accueil":
        main_component()

# Point d'entrée de l'application
if __name__ == "__main__":
    main()
