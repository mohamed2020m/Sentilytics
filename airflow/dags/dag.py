import time
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from pymongo import MongoClient
from datetime import timedelta


# Define MongoDB connection and fetch the first 100 documents
def check_documents():
    client = MongoClient("mongodb://localhost:27017")
    db = client["sentilytics_db"]
    collection = db["sentilytics_collection"]
    # Fetch first 100 documents
    documents = list(collection.find().limit(100))
    if not documents:
        raise ValueError("No documents left to process in MongoDB.")
    return documents
    
# Function to remove the first 100 documents after processing
def remove_documents(documents):
    client = MongoClient("mongodb://localhost:27017")
    db = client["sentilytics_db"]
    collection = db["sentilytics_collection"]
    # Get the _id of documents to delete
    ids_to_delete = [doc['_id'] for doc in documents]
    collection.delete_many({'_id': {'$in': ids_to_delete}})
    print(f"Removed {len(ids_to_delete)} documents from MongoDB.")
    
        
# DAG Definition
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'retries': 0,
}

with DAG(
    'sentilytics_pipeline',
    default_args=default_args,
    description='Pipeline to process and visualize sentilytics pipeline',
    schedule_interval=timedelta(seconds=10),
    catchup=False,
) as dag:

    # Task 1: Verify Documents in MongoDB
    verify_documents = PythonOperator(
        task_id='verify_documents',
        python_callable=check_documents
    )

    # Task 2: Inference and Store in Hive
    inference_store = BashOperator(
        task_id='inference_store',
        bash_command='python ../inference/inference_script.py'
    )

    # Task 3: Remove Processed Documents
    remove_processed_documents = PythonOperator(
        task_id='remove_processed_documents',
        python_callable=remove_documents,
        op_kwargs={'documents': '{{ task_instance.xcom_pull(task_ids="verify_documents") }}'}
    )
    
    # Task dependencies
    verify_documents >> inference_store >> remove_processed_documents