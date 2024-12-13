start:
	docker-compose up -d

start-with-log:
	docker-compose up

# stop:
# 	docker-compose down

add_atlas_to_nifi:
	docker cp ./libs/nifi-atlas-nar-1.9.1.nar nifi_container_persistent:/opt/nifi/nifi-1.19.1/lib

create-kafka-topic:
	docker exec -it kafka_container kafka-topics --create --topic kafka-nifi-dst --bootstrap-server kafka:9093 --partitions 1 --replication-factor 1

copy_atlas_props_to_nifi:
	docker cp atlas_container:/apache-atlas/conf/atlas-application.properties ./tmp_atlas/atlas-application.properties
	docker cp ./tmp_atlas/atlas-application.properties nifi_container_persistent:/opt/nifi/nifi-current/conf/atlas-application.properties

