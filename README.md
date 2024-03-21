# HID Scanner 2 MQTT

1D/2D HID barcode reader to MQTT.

## Getting Started

Prerequisite :

```bash
apt install git python3 python3-pip python3-dev python-is-python3
```

Manual startup :

```bash
pip install -r requirements.txt
python3 hid2mqtt.py
```

NOTE needs a working MQTT broker, mosquitto is a good basic one to try:

```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto.service
```

To test :

```bash
mosquitto_sub -d -t tag_barcode_scan
```

## Install as systemd service (for test env)

To install use following snippet as ROOT (for the moment):

```bash
apt update \
    && apt install git python3 python3-pip python3-dev python-is-python3 \
    && cd /opt \
    && git clone https://github.com/cyril-leclercq/hidscanner2mqtt.git \
    && cd /opt/hidscanner2mqtt \
    && ./setup.sh
```

Logs are available with `journalctl -u hidscanner2mqtt.service`

## Credits

- Based on https://github.com/clach04/keyboard2mqtt
