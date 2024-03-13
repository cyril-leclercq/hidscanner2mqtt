#docker exec -it hidscanner-mosquitto mosquitto_sub -d -t tag_barcode_scan
docker exec -it hidscanner-mosquitto cat /mosquitto/config/mosquitto.conf  