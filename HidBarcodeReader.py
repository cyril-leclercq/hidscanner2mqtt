import constants
import logging
import sys
import evdev
from time import sleep
from configuration import config

class HidBarcodeReader:

    def __init__(self):
        self.log = None
        self.current_device = None
        self.init_logs()

    def init_logs(self):
        self.log  = logging.getLogger(__name__)
        logging.basicConfig()
        self.log.setLevel(level=constants.LOG_LEVEL)
        self.log.info('Python %s on %s', sys.version, sys.platform)

    def log_usb_devices_for_debug(self):
        if logging.getLevelName(self.log) == logging.DEBUG:
            self.log.debug("Listing usb devices...")
            for path in evdev.list_devices():
                tmp_dev = evdev.InputDevice(path)
                self.log.debug('device path %r %r %r %r %r ' % (path, tmp_dev.info, tmp_dev.path, tmp_dev.name, tmp_dev.phys))

    def connect_and_read_hid_device(self, callback_mqtt) :
        while True:
            try:
                self.current_device = self.find_usb_device()
                if self.current_device == None:
                    self.log.info('No device found. Retry in %r s' % constants.USB_DETECTION_DELAY_SECONDS)
                    sleep(constants.USB_DETECTION_DELAY_SECONDS)
                    continue

                self.log.info('Found device path %r' % self.current_device)
                self.read_hid_stream(callback_mqtt)
            except Exception as err:
                logging.warning(err)

    def find_usb_device(self):
        usb_search_list = constants.DEFAULT_USB_DEVICE_LIST
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if (device.info.vendor, device.info.product) in usb_search_list:
                return device
        return None

    def read_hid_stream(self, callback_mqtt):
            try:
                self.current_device.grab()
                while True:
                    (symbology, barcode) = self.keyboard_reader_evdev()
                    callback_mqtt(symbology, barcode)
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

    def try_ungrab(self):
            try:
                if self.current_device != None:
                    self.current_device.ungrab()
            except Exception as err:
                logging.warning(err)