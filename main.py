#!/usr/bin/env python

import sys
import logging
import paho.mqtt.publish as publish
import constants
from configuration import config
from Hid2Mqtt import Hid2Mqtt

log  = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(level=constants.LOG_LEVEL)

def callback_mqtt(symbology, barcode):
    try:
        log.debug('MQTT send: %r' % barcode)
        mqtt_message = barcode
        result =  publish.single(config['mqtt_topic'], mqtt_message, hostname=config['mqtt_broker'], port=config['mqtt_port'])
        log.debug('mqqt publish result %r', result)  # returns None on success, on failure exception
    except Exception as e:
        log.error('Failed to upload to MQTT: %s', repr(e))

if __name__ == "__main__":
    hid2Mqtt = Hid2Mqtt()
    hid2Mqtt.log_usb_devices_for_debug()
    hid2Mqtt.connect_and_read_hid_device(callback_mqtt)
    sys.exit(0)
