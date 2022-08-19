from usbscanner import USBScanner
from lcd1602 import LCD1602
from ultrasonic import Ultrasonic
from mqtt import Mqtt
from gate import Gate
from helper import Helper
from db import DB

import time
import base64

MACHINE_ID = "TEST01"

class Main():
    def __init__(self):
        self.lcd = LCD1602()
        self.ultrasonic = Ultrasonic(echo_pin=27, trigger_pin=17)
        # NOTE: path to USB device when it's already plugged will be at /dev/input/event0
        # if it plugged after raspi up, it will be at /dev/input/event1
        device_path = "/dev/input/event0"
        self.usb_scanner = USBScanner(device_path)
        # Gate take device_path too, but since it's only 1 device_path
        # i think it's ok to use the default one /dev/ttyAMA0
        self.gate = Gate()
        Helper.log_print("Parking IoT start")
        self.mqtt = Mqtt(host="172.104.182.166", port=1883, keepalive=60, username="testparking", password="123456")
        self.db = DB("scanned.db")

        Helper.log_print("initilaize gate")
        # uncomment one of initialization below to choose between gate entry and exit
        # self.gate_entry()
        # self.gate_exit()

    def gate_entry(self):
        while True:
            # 1. print waiting for QR Scan message
            self.lcd.waiting_message()
            try:
                scanned_string = self.usb_scanner.readQRCode()
                scanned_string = base64.b64decode(scanned_string)
                # take scanned string > check the command (checkin, checkout)
                # if checkin, just directly open the gate, 
                json_data = Helper.parse_json_qrcode(scanned_string)
                if not json_data['parking_type'] == "checkin":
                    continue
                self.db.insert_data({json_data})
                self.mqtt.publish_command(MACHINE_ID, json_data['parking_type'], json_data)
                # print message selamat datang
                self.lcd.scan_success_message(gate=0)
                # open gate parking
                Helper.log_print("checkin success")
                self.gate.open_gate()

                # when vehicle passing the gate, loop to first step
                if self.ultrasonic.is_vehicle_pass():
                    Helper.log_print("vehicle passing the gate")
                    self.gate.close_gate()
            except Exception as e:
                Helper.log_print(e)
    
    def gate_exit(self):
        while True:
            # 1. print waiting for QR Scan message
            self.lcd.waiting_message()
            try:
                scanned_string = self.usb_scanner.readQRCode()
                scanned_string = base64.b64decode(scanned_string)
                # take scanned string > check the command (checkin, checkout)
                # if checkin, just directly open the gate, 
                # if checkout, check expired time first before open the gate
                # when checkout and expired time > time_now, print expired message
                json_data = Helper.parse_json_qrcode(scanned_string)
                if json_data['parking_type'] not in ['recheckin', 'checkout']:
                    continue
                else:
                    self.db.insert_data({json_data})
                    expired_time = Helper.parse_datetime(json_data['expired'])
                    if Helper.parse_to_timestamp(date=expired_time) > Helper.parse_to_timestamp():
                        # When expired time is more than current time, print expired message
                        self.lcd.expired_message()
                        Helper.log_print("expired")
                        time.sleep(5)
                        # and continue to first step waiting for QR Scan
                        continue

                if json_data['parking_type'] == 'recheckin':
                    self.mqtt.publish_command(MACHINE_ID, json_data['parking_type'], json_data)
                    # print message selamat datang
                    self.lcd.scan_success_message(gate=0)
                    Helper.log_print("recheckin success")
                    continue
                else:
                    expired_time = Helper.parse_datetime(json_data['expired'])
                    if Helper.parse_to_timestamp(date=expired_time) < Helper.parse_to_timestamp():
                        # When expired time is more than current time, print expired message
                        self.lcd.expired_message()
                        Helper.log_print("expired")
                        time.sleep(5)
                        # and continue to first step waiting for QR Scan
                        continue

                    self.lcd.scan_success_message(gate=1)
                    self.mqtt.publish_command(MACHINE_ID, json_data['parking_type'], json_data)
                    Helper.log_print("checkout success")
                    self.gate.open_gate()

                # when vehicle passing the gate, loop to first step
                if self.ultrasonic.is_vehicle_pass():
                    Helper.log_print("vehicle passing the gate")
                    self.gate.close_gate()
            except Exception as e:
                Helper.log_print(e)

if __name__ == '__main__':
    main = Main()
