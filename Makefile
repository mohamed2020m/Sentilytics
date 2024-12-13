start:
	docker-compose up -d

start-with-log:
	docker-compose up

stop:
	docker-compose down

# atlas
add_atlas_to_nifi:
	docker cp ./libs/nifi-atlas-nar-1.9.1.nar nifi_container_persistent:/opt/nifi/nifi-1.19.1/lib

# create kafka topic
create_kafka_topic:
	docker exec -it kafka_container kafka-topics --create --topic kafka-nifi-dst --bootstrap-server kafka:9093 --partitions 1 --replication-factor 1

# create kafka topic
list_kafka_topic:
	docker exec -it kafka_container kafka-topics --list --bootstrap-server kafka:9093

# nifi with atlas
copy_atlas_props_to_nifi:
	docker cp atlas_container:/apache-atlas/conf/atlas-application.properties ./tmp_atlas/atlas-application.properties
	docker cp ./tmp_atlas/atlas-application.properties nifi_container_persistent:/opt/nifi/nifi-current/conf/atlas-application.properties

# Test nifi-kafka connection
conf_test:
	docker cp ./f914bab7-d46d-4c1d-b2c1-aa8c699958ef  nifi_container_persistent:/opt/nifi/test.json



