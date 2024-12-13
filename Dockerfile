FROM apache/airflow:2.9.3

# Install custom Python modules
RUN pip install pymongo