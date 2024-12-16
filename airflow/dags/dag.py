from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from datetime import datetime
import pandas as pd
from pymongo import MongoClient
from pyhive import TextBlob
from pyhive import hive

# Définition des fonctions utilisées
def get_data_from_mongo(**kwargs):
    try:
        mongo_client = MongoClient('mongodb://root:root@mongo:27017')
        mongo_db = mongo_client['comments_db']
        mongo_collection = mongo_db['comments']
        data = list(mongo_collection.find().limit(100))

        df = pd.DataFrame(data)
        kwargs['ti'].xcom_push(key='dataframe', value=df)
        return "Data fetched from MongoDB"
    except Exception as e:
        print("Erreur lors de la connexion à MongoDB ou de la récupération des données :", e)
        raise e

def get_sentiment_and_save_csv(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(key='dataframe', task_ids='fetch_data')
    if df is not None and not df.empty:
        df["Sentiment_Pred"] = df["textOriginal"].apply(get_sentiment)
        df.to_csv("output_with_sentiment.csv", index=False)
        ti.xcom_push(key='processed_df', value=df)
        return "Sentiment predicted and CSV saved"
    else:
        print("Aucune donnée disponible pour le traitement.")
        raise ValueError("No data available for processing")

def get_sentiment(text):
    if pd.notnull(text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            return "positive"
        elif polarity < 0:
            return "negative"
        else:
            return "neutral"
    else:
        return "neutral"

def save_to_hive(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(key='processed_df', task_ids='process_sentiment')
    try:
        connection = hive.connect(
            host='hive',
            port=9083,
            username='hive',
            auth='NOSASL')
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS comments_sentiment (
            source STRING,
            textOriginal STRING,
            likeCount INT,
            publishedAt DATE,
            channel STRING,
            prediction STRING
        )
        STORED AS PARQUET
        """
        cursor.execute(create_table_query)

        parquet_file = "output_with_sentiment.parquet"
        df.to_parquet(parquet_file, index=False)

        load_data_query = f"LOAD DATA LOCAL INPATH '{parquet_file}' INTO TABLE comments_sentiment"
        cursor.execute(load_data_query)
        return "Data saved to Hive"
    except Exception as e:
        print("Erreur lors de l'enregistrement dans Hive :", e)
        raise e

def remove_data_from_mongo(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(key='processed_df', task_ids='process_sentiment')
    client = MongoClient("mongodb://root:root@mongo:27017")
    db = client["comments_db"]
    collection = db["comments"]
    ids_to_delete = df['_id'].tolist()
    collection.delete_many({'_id': {'$in': ids_to_delete}})
    return "Data removed from MongoDB"  


# DAG Definition
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'retries': 0,
}

with DAG(
    'mongo_inference_pipeline',
    default_args=default_args,
    description='Pipeline to process and visualize MongoDB data every 30 seconds',
    schedule_interval=timedelta(seconds=10),
    catchup=False,
) as dag:

    # Task 1: Récupération des données de MongoDB
    fetch_data = PythonOperator(
        task_id='fetch_data',
        python_callable=get_data_from_mongo,
        provide_context=True
    )

    # Task 2: Analyse des sentiments et sauvegarde en CSV
    process_sentiment = PythonOperator(
        task_id='process_sentiment',
        python_callable=get_sentiment_and_save_csv,
        provide_context=True
    )

    # Task 3: Sauvegarde des données dans Hive
    save_hive = PythonOperator(
        task_id='save_to_hive',
        python_callable=save_to_hive,
        provide_context=True
    )

    # Task 5: Suppression des données traitées dans MongoDB
    cleanup_mongo = PythonOperator(
        task_id='cleanup_mongo',
        python_callable=remove_data_from_mongo,
        provide_context=True
    )

    # Task dependencies
    fetch_data >> process_sentiment >> save_hive >> cleanup_mongo
    