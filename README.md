# keyboard2mqtt

RFID tag reader and 1D/2D barcode reader to MQTT - or any device that emulates a HID USB Keyboard with newline as the terminator.

In theory any (real) keyboard could be captured, not just a device that emulates a keyboard.

## Getting Started

NOTE needs a working MQTT broker, mosquitto is a good basic one to try:

    sudo apt update
    sudo apt install -y mosquitto mosquitto-clients
    sudo systemctl enable mosquitto.service

If installing/working with a source checkout issue:

    pip install -r requirements.txt

## Credits

  * Based on https://github.com/clach04/keyboard2mqtt 
