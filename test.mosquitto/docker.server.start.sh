docker run --rm -it \
    -p 1883:1883 \
    -p 9001:9001 \
    -p 8080:8080 \
    -v $(pwd)/config:/mosquitto/config \
    --name hidscanner-mosquitto eclipse-mosquitto