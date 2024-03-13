# HID Scanner 2 MQTT

1D/2D HID barcode reader to MQTT.

## Getting Started

Manual startup :

    pip install -r requirements.txt
    python3 hid2mqtt.py

NOTE needs a working MQTT broker, mosquitto is a good basic one to try:

    sudo apt update
    sudo apt install -y mosquitto mosquitto-clients
    sudo systemctl enable mosquitto.service

## Install as systemd service

To install use following snippet :

    cd /opt \
        && sudo git clone https://github.com/cyril-leclercq/hidscanner2mqtt.git \
        && cd /opt/hidscanner2mqtt \
        && sudo ./setup.sh

Logs are available with `journalctl -u hidscanner2mqtt.service`

## Credits

- Based on https://github.com/clach04/keyboard2mqtt
