# HID Scanner 2 MQTT

1D/2D HID barcode reader to MQTT.

## Getting Started

NOTE needs a working MQTT broker, mosquitto is a good basic one to try:

    sudo apt update
    sudo apt install -y mosquitto mosquitto-clients
    sudo systemctl enable mosquitto.service

If installing/working with a source checkout issue:

    pip install -r requirements.txt

## Credits

- Based on https://github.com/clach04/keyboard2mqtt
