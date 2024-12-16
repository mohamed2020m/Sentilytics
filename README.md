
# Sentilytics : 

**Data Governance and Metadata Management in a Data Pipeline Using Apache Atlas within a Lambda Architecture**


## Project Pipeline

![project_piepline](./assets/images/project_piepline.png)

## DESCRIPTION

This project focuses on designing and implementing a comprehensive big data pipeline that adheres to the principles of Lambda Architecture, ensuring real-time and batch processing capabilities while maintaining robust data governance and metadata management using Apache Atlas.  

#### **Project Overview**  
1. **Data Sources:**  
   - **YouTube API:** Streams video-related data, enabling analysis of trends and public sentiment in media content.  
   - **New York Times API:** Streams news articles and metadata, offering insights into public sentiment across various topics.  

2. **Sentiment Analysis Model:**  
   - A financial sentiment analysis model is trained using a labeled dataset from Kaggle: [Financial Sentiment Analysis](https://www.kaggle.com/datasets/sbhatti/financial-sentiment-analysis).  
   - The trained model is applied to streaming and batch data to analyze sentiments expressed in the incoming text from the two data sources.  

3. **Lambda Architecture Implementation:**  
   - **Batch Layer:**  
     - **Apache Spark:** Handles large-scale data processing for historical data analysis.  
     - **Apache Hive:** Stores processed, structured data and acts as a central data warehouse.  
     - **Spark ML:** Supports the training of the sentiment analysis model.  
   - **Speed Layer:**  
     - **Spark Streaming:** Processes streaming data in real-time from the YouTube and New York Times APIs.  
     - **Apache NiFi:** Facilitates data validation, transformation, and the merging of data streams from both sources, ensuring data quality and consistency.
      - **mongodb**: For storing processed data from sprak streaming 
   - **Serving Layer:**  
     - **Apache Parquet:** Provides optimized storage for data views, enabling efficient querying.  
     - **Streamlit:** A visualization tool for monitoring and exploring the processed data in real-time.  
     - **Apache Zeppelin:** Supports advanced analytics and visualization for exploratory data analysis.  

4. **Data Governance and Lineage:**  
   - **Apache Atlas:** Ensures end-to-end governance and metadata management of the data pipeline. This includes tracking data lineage (e.g., origin, transformations, and usage) and providing visibility into the lifecycle of data as it flows through the pipeline.  

5. **Workflow Orchestration:**  
   - **Apache Airflow:** Orchestrates and automates the various tasks in the pipeline.  

#### **Key Outcomes:**  
- Real-time sentiment insights from streaming data sources.  
- Scalable and efficient batch processing for historical data.  
- Seamless integration of governance and metadata management to enhance traceability and compliance.  
- An interactive dashboard for data visualization and analysis.  

## Requirements
- Docker and Docker Compose
- Minimum 16GB RAM recommended
- [Make](https://gnuwin32.sourceforge.net/packages/make.htm)
- Python >= 3.10

## Installation

1. clone the project.

```bash
git clone https://github.com/mohamed2020m/Sentilytics
```

2. Run docker compose 

```bash
make start
```

## Get Your keys

Please follow the detailed instructions in our report on how to obtain API keys from Google Cloud and The New York Times.

## Nifi & Kafka configuration

Create new topic `kafka-nifi-dst` using the following command:

```bash
make create_kafka_topic
```

Verify `kafka-nifi-dst` topic creation

```bash
make list_kafka_topic
```

**Note:** YOU HAVE TO UPDATE KAFKA PROCESSOR IN NIFI TO USE YOU'RE IP LOCAL. 

For more info check our article.

## Nifi & Atlas configuration

Add nifi-atlas NAR to nifi container

```bash
make add_atlas_to_nifi
```

## Test Nifi-Kafka communication

To test Nifi-kafka communication follow these steps:
1. Go to `tests` folder

2. run the following command:
```bash
make conf_test
```
This will copy the dummy json file `f914bab7-d46d-4c1d-b2c1-aa8c699958e` to the `nifi_container_persistent` container

3. Open apache nifi by visting `http://localhost:8091/nifi/` 

4. Add a new proccessor `GetFile` and configurate like this:

![GetFile_Processor_Configuration](./assets/images/GetFile_Processor_Configuration.png)

5. Connect it to `PublishKafka_2_0` proccessor
like this: 
![GetFile_with_PublishKafka_2_0](./assets/images/GetFile_with_PublishKafka_2_0.png)

6. Run the `kafka_consumer.py` script

7. Go back to nifi and start only these two proccesors

8. Finnaly, verify you're terminal you will see something like this:
![kafka_consumer_response](./assets/images/kafka_consumer_response.png)



## Model Training


1. Make sure that the Zipline service is running and exposed on port 8085. You can check this by verifying the container where Zipline is deployed.
2. To open the Zipline web interface, enter the following URL in the browser's address bar :
```bash
http://localhost:8085/ 
```
3. Import the SentimentAnalysis notebook located in the `models` folder.
4. Run the SentimentAnalysis notebook to explore the different steps we used for selecting the best classification model to use.
5. We use MLflow for tracking our machine learning models, which helps us compare different versions and evaluate their performance. MLflow enables us to track experiments by recording metrics, parameters, and output files for each run.

   To access the MLflow web UI and compare different metrics, use the following command:
```bash
mlflow ui -p 1234
```











## Real-time Visualization using Streamlit

### Pre-installation

```bash
pip install -r requirements.txt
```
### Set-up

Create a file called .env and fill in the following content
```bash
HOST=localhost
PORT=10000
USER=hive
PASSWORD=your_password
DATABASE=Hive_database
```

### Stream the complex visualization
To perform streaming processing on the dashboard, you need to deploy all the settings mentioned above, as well as ensure that the entire pipeline is functioning correctly and all its components are in place.

### Run 
To start the visualization of historical data and real-time predictions, run the following command:

```bash
streamlit run app.py --server.port 8502
```

## Video Demo

Click [here](https://drive.google.com/file/d/13sxlESQgW1Z_gMACT10qyb2f2WIebrEa/view?usp=drive_link) to watch the video demo on Google Drive.








