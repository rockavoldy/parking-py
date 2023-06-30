from usbscanner import USBScanner
from lcd1602 import LCD1602
from ultrasonic import Ultrasonic
from mqtt import Mqtt
from gate import Gate
from helper import Helper
from db import DB

import time
import base64
import os

MACHINE_ID = "TEST01"
MQTT_HOST = os.getenv('PARK_MQTT_HOST', 'localhost')
MQTT_PORT = os.getenv('PARK_MQTT_PORT', 1883)
MQTT_USER = os.getenv('PARK_MQTT_USER', 'testparking')
MQTT_PASS = os.getenv('PARK_MQTT_PASS', '123456')

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
        self.mqtt = Mqtt(host=MQTT_HOST, port=MQTT_PORT, keepalive=60, username=MQTT_USER, password=MQTT_PASS)
        self.db = DB("scanned.db")

        Helper.log_print("initilaize gate")

    def gate_entry(self):
        Helper.log_print("Gate entry ready!")
        while True:
            # 1. print waiting for QR Scan message
            self.lcd.waiting_message()
            try:
                Helper.log_print("Waiting for QR")
                scanned_string = self.usb_scanner.readQRCode()
                scanned_string = base64.b64decode(scanned_string)
                # take scanned string > check the command (checkin, checkout)
                # if checkin, just directly open the gate, 
                json_data = Helper.parse_json_qrcode(scanned_string)
                if not json_data['parking_type'] == "checkin":
                    continue
                if self.db.get_count_data(code=json_data['code'], parking_type=json_data['parking_type']) == 0:
                    Helper.log_print("Invalid QR Code for checkin")
                    self.lcd.invalid_qr_message()
                    continue
                self.db.insert_data({'parking_type': json_data['parking_type'], 'code': json_data['code']})
                self.mqtt.publish_command(MACHINE_ID, json_data['parking_type'], json_data)
                # print message selamat datang
                self.lcd.scan_success_message(gate=0)
                # open gate parking
                Helper.log_print("Checkin success")
                self.gate.open_gate()

                # when vehicle passing the gate, loop to first step
                if self.ultrasonic.is_vehicle_pass():
                    Helper.log_print("Vehicle passing the gate")
                    self.gate.close_gate()
            except Exception as e:
                Helper.log_print(e)
    
    def gate_exit(self):
        Helper.log_print("Gate Exit ready!")
        while True:
            # 1. print waiting for QR Scan message
            self.lcd.waiting_message()
            try:
                Helper.log_print("Waiting for QR")
                scanned_string = self.usb_scanner.readQRCode()
                scanned_string = base64.b64decode(scanned_string)
                # take scanned string > check the command (checkin, checkout)
                # if checkin, just directly open the gate, 
                # if checkout, check expired time first before open the gate
                # when checkout and expired time > time_now, print expired message
                json_data = Helper.parse_json_qrcode(scanned_string)
                parking_type = json_data['parking_type']
                if parking_type not in ['recheckin', 'checkout']:
                    continue

                if self.db.get_count_data(code=json_data['code'], parking_type=json_data['parking_type']) > 0:
                    Helper.log_print("Invalid QR Code for recheckin or checkout")
                    self.lcd.invalid_qr_message()
                    continue
                self.db.insert_data({'parking_type': parking_type, 'code': json_data['code']})

                if parking_type == 'recheckin':
                    self.mqtt.publish_command(MACHINE_ID, parking_type, json_data)
                    self.lcd.recheckin_message()
                    Helper.log_print("Recheckin success")
                    continue

                expired_time = Helper.parse_datetime(json_data['expired'])
                expired_timestamp = Helper.parse_to_timestamp(date=expired_time)
                Helper.log_print(f"expired_time: {expired_timestamp}")
                now_timestamp = Helper.parse_to_timestamp()
                Helper.log_print(f"current_time: {now_timestamp}")
                # If expired_timestamp already passed by now_timestamp
                if expired_timestamp < now_timestamp:
                    Helper.log_print(f"Expired < Current: {expired_timestamp} < {now_timestamp}")
                    self.lcd.expired_message()
                    Helper.log_print("QR Expired")
                    time.sleep(5)
                    # and continue to first step waiting for QR Scan
                    continue

                self.lcd.scan_success_message(gate=1)
                self.mqtt.publish_command(MACHINE_ID, parking_type, json_data)
                Helper.log_print("Checkout success")
                self.gate.open_gate()

                # when vehicle passing the gate, loop to first step
                if self.ultrasonic.is_vehicle_pass():
                    Helper.log_print("Vehicle passing the gate")
                    self.gate.close_gate()
            except Exception as e:
                Helper.log_print(e)

if __name__ == '__main__':
    main = Main()
    # uncomment one of initialization below to choose between gate entry and exit
    # main.gate_entry()
    # main.gate_exit()
