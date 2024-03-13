import constants
import logging
import sys
import evdev
import paho.mqtt.publish as publish
from time import sleep
from configuration import config

class Hid2Mqtt:

    def __init__(self):
        self.log = None
        self.current_device = None
        self.init_logs()

    def init_logs(self):
        self.log  = logging.getLogger(__name__)
        logging.basicConfig()
        self.log .setLevel(level=constants.LOG_LEVEL)
        self.log .info('Python %s on %s', sys.version, sys.platform)

    def log_usb_devices_for_debug(self):
        if logging.getLevelName(self.log) == logging.DEBUG:
            self.log.debug("Listing usb devices...")
            for path in evdev.list_devices():
                tmp_dev = evdev.InputDevice(path)
                self.log.debug('device path %r %r %r %r %r ' % (path, tmp_dev.info, tmp_dev.path, tmp_dev.name, tmp_dev.phys))

    def connect_and_read_hid_device(self) :
        while True:
            try:
                current_device = self.find_usb_device()
                if current_device == None:
                    self.log.info('No device found. Retry in %r s' % constants.USB_DETECTION_DELAY_SECONDS)
                    sleep(constants.USB_DETECTION_DELAY_SECONDS)
                    continue

                self.log.info('Found device path %r' % current_device)
                self.read_hid_stream()
            except Exception as err:
                logging.warning(err)

    def find_usb_device(self):
        usb_search_list = constants.DEFAULT_USB_DEVICE_LIST
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if (device.info.vendor, device.info.product) in usb_search_list:
                return device
        return None

    def read_hid_stream(self):
            try:
                self.current_device.grab()
                while True:
                    read_string = self.keyboard_reader_evdev(self.current_device)
                    self.callback_mqtt(read_string)
            except Exception as err:
                logging.warning(repr(err))
            finally:
                self.try_ungrab()

    def keyboard_reader_evdev(self):
        barcode_string_output = ''
        barcode_symbology = ''
        shift_active = False
        for event in self.current_device.read_loop():
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

    def callback_mqtt(self, input_string):
        try:
            (symbology, barcode) = input_string
            self.log.debug('MQTT send: %r' % barcode)
            mqtt_message = barcode
            # initial payload trivial, just the keypresses with terminator (newline) removed
            # no announcements, no timestamps, so client details
            result =  publish.single(config['mqtt_topic'], mqtt_message, hostname=config['mqtt_broker'], port=config['mqtt_port'])
            self.log.debug('mqqt publish result %r', result)  # returns None on success, on failure exception
        except Exception as e:
            self.log.error('Failed to upload to MQTT: %s', repr(e))

    def try_ungrab(self):
            try:
                if self.current_device != None:
                    self.current_device.ungrab()
            except Exception as err:
                logging.warning(err)