#!/usr/bin/env python

import json
import logging
import os
import sys
import evdev
import paho.mqtt.publish as publish

from time import sleep


version_tuple = (0, 0, 1)
version = version_string = __version__ = '%d.%d.%d' % version_tuple

log = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(level=logging.DEBUG)

log.info('Python %s on %s', sys.version, sys.platform)

USB_DETECTION_DELAY_SECONDS = 1

DEFAULT_USB_DEVICE_LIST = [
    (1504, 4608), # Symbol Technologies, Inc, 2008 Symbol Bar Code Scanner
]

def find_usb_device(usb_search_list=None):
    usb_search_list = usb_search_list or DEFAULT_USB_DEVICE_LIST
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if (device.info.vendor, device.info.product) in usb_search_list:
            return device
    return None


ERROR_CHARACTER = '?'
VALUE_UP = 0
VALUE_DOWN = 1

CHARMAP = {
        evdev.ecodes.KEY_1: ['1', '!'],
        evdev.ecodes.KEY_2: ['2', '@'],
        evdev.ecodes.KEY_3: ['3', '#'],
        evdev.ecodes.KEY_4: ['4', '$'],
        evdev.ecodes.KEY_5: ['5', '%'],
        evdev.ecodes.KEY_6: ['6', '^'],
        evdev.ecodes.KEY_7: ['7', '&'],
        evdev.ecodes.KEY_8: ['8', '*'],
        evdev.ecodes.KEY_9: ['9', '('],
        evdev.ecodes.KEY_0: ['0', ')'],
        evdev.ecodes.KEY_MINUS: ['-', '_'],
        evdev.ecodes.KEY_EQUAL: ['=', '+'],
        evdev.ecodes.KEY_TAB: ['\t', '\t'],
        evdev.ecodes.KEY_Q: ['q', 'Q'],
        evdev.ecodes.KEY_W: ['w', 'W'],
        evdev.ecodes.KEY_E: ['e', 'E'],
        evdev.ecodes.KEY_R: ['r', 'R'],
        evdev.ecodes.KEY_T: ['t', 'T'],
        evdev.ecodes.KEY_Y: ['y', 'Y'],
        evdev.ecodes.KEY_U: ['u', 'U'],
        evdev.ecodes.KEY_I: ['i', 'I'],
        evdev.ecodes.KEY_O: ['o', 'O'],
        evdev.ecodes.KEY_P: ['p', 'P'],
        evdev.ecodes.KEY_LEFTBRACE: ['[', '{'],
        evdev.ecodes.KEY_RIGHTBRACE: [']', '}'],
        evdev.ecodes.KEY_A: ['a', 'A'],
        evdev.ecodes.KEY_S: ['s', 'S'],
        evdev.ecodes.KEY_D: ['d', 'D'],
        evdev.ecodes.KEY_F: ['f', 'F'],
        evdev.ecodes.KEY_G: ['g', 'G'],
        evdev.ecodes.KEY_H: ['h', 'H'],
        evdev.ecodes.KEY_J: ['j', 'J'],
        evdev.ecodes.KEY_K: ['k', 'K'],
        evdev.ecodes.KEY_L: ['l', 'L'],
        evdev.ecodes.KEY_SEMICOLON: [';', ':'],
        evdev.ecodes.KEY_APOSTROPHE: ['\'', '"'],
        evdev.ecodes.KEY_BACKSLASH: ['\\', '|'],
        evdev.ecodes.KEY_Z: ['z', 'Z'],
        evdev.ecodes.KEY_X: ['x', 'X'],
        evdev.ecodes.KEY_C: ['c', 'C'],
        evdev.ecodes.KEY_V: ['v', 'V'],
        evdev.ecodes.KEY_B: ['b', 'B'],
        evdev.ecodes.KEY_N: ['n', 'N'],
        evdev.ecodes.KEY_M: ['m', 'M'],
        evdev.ecodes.KEY_COMMA: [',', '<'],
        evdev.ecodes.KEY_DOT: ['.', '>'],
        evdev.ecodes.KEY_SLASH: ['/', '?'],
        evdev.ecodes.KEY_SPACE: [' ', ' '],
}

def keyboard_reader_evdev(dev):
    barcode_string_output = ''
    barcode_symbology = ''
    shift_active = False
    for event in dev.read_loop():
        if event.code == evdev.ecodes.KEY_ENTER and event.value == VALUE_DOWN:
            return (barcode_symbology, barcode_string_output)
        elif event.code == evdev.ecodes.KEY_LEFTSHIFT or event.code == evdev.ecodes.KEY_RIGHTSHIFT:
            shift_active = event.value == VALUE_DOWN
        elif event.value == VALUE_DOWN:
            ch = CHARMAP.get(event.code, ERROR_CHARACTER)[1 if shift_active else 0]
            if barcode_symbology == '':
                barcode_symbology = ch
            else:
                barcode_string_output += ch

def main(argv=None):
    print('Python %r on %r' % (sys.version, sys.platform))

    config = {
        'debug': True,
        'use_symbology_prefix' : False,
        'mqtt_broker': 'localhost',
        'mqtt_port': 1883,
        'mqtt_topic': 'tag_keyboard_reader',  # to monitor, issue: mosquitto_sub -t tag_keyboard_reader
    }

    print(json.dumps(config, indent=4))
    if config['debug']:
        log.setLevel(level=logging.DEBUG)
    else:
        log.setLevel(level=logging.INFO)

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

    def print_usb_devices():
        log.debug("Listing usb devices...")
        for path in evdev.list_devices():
            tmp_dev = evdev.InputDevice(path)
            log.info('device path %r %r %r %r %r ' % (path, tmp_dev.info, tmp_dev.path, tmp_dev.name, tmp_dev.phys))

    def read_hid_stream(dev):
            try:
                dev.grab()
                while True:
                    read_string = keyboard_reader_evdev(dev)
                    callback_mqtt(read_string)
            except KeyboardInterrupt:
                logging.debug('Keyboard interrupt')
            except Exception as err:
                logging.error(err)
            finally:
                try_ungrab(dev)

    def try_ungrab(dev):
            try:
                dev.ungrab()
            except Exception as err:
                logging.warn(err)
            finally:
                dev.ungrab()

    def connect_and_read_hid_device() :
        while True:
            try:
                dev = find_usb_device()
                if dev == None:
                    log.info('No device found. Retry in %r s' % USB_DETECTION_DELAY_SECONDS)
                    sleep(USB_DETECTION_DELAY_SECONDS)
                    continue

                log.info('Found device path %r' % dev)
                read_hid_stream(dev)
            except Exception as err:
                logging.warn(err)

    print_usb_devices()
    connect_and_read_hid_device()

if __name__ == "__main__":
    sys.exit(main())