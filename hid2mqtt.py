#!/usr/bin/env python

import constants
import logging
import sys
import evdev
import sys, signal
import paho.mqtt.publish as publish

from time import sleep
from configuration import config

version_tuple = (0, 0, 1)
version = version_string = __version__ = '%d.%d.%d' % version_tuple

log = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(level=logging.DEBUG)
log.info('Python %s on %s', sys.version, sys.platform)

def main(argv=None):
    print_usb_devices()
    connect_and_read_hid_device()

def print_usb_devices():
        log.debug("Listing usb devices...")
        for path in evdev.list_devices():
            tmp_dev = evdev.InputDevice(path)
            log.debug('device path %r %r %r %r %r ' % (path, tmp_dev.info, tmp_dev.path, tmp_dev.name, tmp_dev.phys))

def connect_and_read_hid_device() :
    while True:
        try:
            dev = find_usb_device()
            if dev == None:
                log.info('No device found. Retry in %r s' % constants.USB_DETECTION_DELAY_SECONDS)
                sleep(constants.USB_DETECTION_DELAY_SECONDS)
                continue

            log.info('Found device path %r' % dev)
            read_hid_stream(dev)
        except Exception as err:
            logging.warning(repr(err))

def find_usb_device(usb_search_list=None):
    usb_search_list = usb_search_list or constants.DEFAULT_USB_DEVICE_LIST
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if (device.info.vendor, device.info.product) in usb_search_list:
            return device
    return None

def read_hid_stream(dev):
        try:
            dev.grab()
            while True:
                read_string = keyboard_reader_evdev(dev)
                callback_mqtt(read_string)
        except Exception as err:
            logging.warning(repr(err))
        finally:
            try_ungrab(dev)

def keyboard_reader_evdev(dev):
    barcode_string_output = ''
    barcode_symbology = ''
    shift_active = False
    for event in dev.read_loop():
        if event.code == evdev.ecodes.KEY_ENTER and event.value == constants.VALUE_DOWN:
            return (barcode_symbology, barcode_string_output)
        elif event.code == evdev.ecodes.KEY_LEFTSHIFT or event.code == evdev.ecodes.KEY_RIGHTSHIFT:
            shift_active = event.value == constants.VALUE_DOWN
        elif event.value == constants.VALUE_DOWN:
            ch = constants.CHARMAP.get(event.code, constants.ERROR_CHARACTER)[1 if shift_active else 0]
            if barcode_symbology == '':
                barcode_symbology = ch
            else:
                barcode_string_output += ch

def callback_mqtt(input_string):
    try:
        (symbology, barcode) = input_string
        log.debug('MQTT send: %r' % barcode)
        mqtt_message = barcode
        # initial payload trivial, just the keypresses with terminator (newline) removed
        # no announcements, no timestamps, so client details
        result =  publish.single(config['mqtt_topic'], mqtt_message, hostname=config['mqtt_broker'], port=config['mqtt_port'])
        log.debug('mqqt publish result %r', result)  # returns None on success, on failure exception
    except Exception as e:      # works on python 3.x
        log.error('Failed to upload to MQTT: %s', repr(e))

def try_ungrab(dev):
        try:
            dev.ungrab()
        except Exception as err:
            logging.warning(err)
        finally:
            dev.ungrab()
            
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    sys.exit(main())