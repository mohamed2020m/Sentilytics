
# Sentilytics

TODO: 

DESCRIPTION


![project_piepline](./assets/images/project_piepline.png)


## Installation

TODO:

## Nifi & Kafka configuration

Create new topic `kafka-nifi-dst` using the following command:

```bash
make create_kafka_topic
```

Verify `kafka-nifi-dst` topic creation

```bash
make list_kafka_topic
```

## Nifi & Atlas configuration


1. export your IP private as a variable;

```powershell
$IP = (Get-NetIPAddress -InterfaceAlias "Ethernet" | Where-Object { $_.AddressFamily -eq 'IPv4' }).IPAddress
```

using bash

```
export IP=$(ipconfig getifaddr en0)
```

this for nifi with atlas

```bash
docker cp ./lib/nifi-atlas-nar-1.19.0.nar nifi_container_persistent:/opt/nifi/nifi-1.19.1/lib
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
