FROM apache/airflow:2.9.3

# Install pymongo
RUN pip install pymongo pyhive pyhive pandas