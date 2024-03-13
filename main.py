#!/usr/bin/env python

import sys
from Hid2Mqtt import Hid2Mqtt

if __name__ == "__main__":
    hid2Mqtt = Hid2Mqtt()
    hid2Mqtt.log_usb_devices_for_debug()
    hid2Mqtt.connect_and_read_hid_device()
    sys.exit(0)
