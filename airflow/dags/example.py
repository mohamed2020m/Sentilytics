from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

def greetings():
    print("Hello World!")
    
def say_goodbye():
    print("Goodbye World!")
    
# DAG Definition
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'retries': 0
}

with DAG(
    'mongo_inference_pipeline',
    default_args=default_args,
    description='Pipeline to process and visualize MongoDB data every 30 seconds',
    schedule_interval=timedelta(seconds=10),
    catchup=False,
) as dag:
    
    greetings_task = PythonOperator(
        task_id='task_1',
        python_callable=greetings
    )
    
    
    say_goodbye_task = PythonOperator(
        task_id='task_2',
        python_callable=say_goodbye
    )
    
    greetings_task >> say_goodbye_task
    
    
