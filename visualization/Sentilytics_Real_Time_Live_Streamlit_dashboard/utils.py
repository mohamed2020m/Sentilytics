from pyhive import hive
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

host = os.getenv('HOST')
port = os.getenv('PORT')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')

#Connexion a hive
def get_hive_connection():
    try:
        conn = hive.Connection(host=host, port=port, username=user, database=database)
        return conn
    except Exception as e:
        st.error(f"Error connecting to Hive: {e}")
        return None  