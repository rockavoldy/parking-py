from usbscanner import USBScanner
from lcd1602 import LCD1602
from ultrasonic import Ultrasonic
from mqtt import Mqtt
from gate import Gate
from helper import Helper
import base64

MACHINE_ID = "TEST01"

class Main():
    def __init__(self):
        lcd = LCD1602()
        ultrasonic = Ultrasonic(echo_pin=17, trigger_pin=27)
        # NOTE: path to USB device when it's already plugged will be at /dev/input/event0
        # if it plugged after raspi up, it will be at /dev/input/event1
        device_path = "/dev/input/event0"
        usb_scanner = USBScanner(device_path)
        # Gate take device_path too, but since it's only 1 device_path
        # i think it's ok to use the default one /dev/ttyAMA0
        gate = Gate()
        print("Parking IoT start")
        mqtt = Mqtt(host="api.akhmad.id", port=1883, keepalive=60, username="testparking", password="123456")
        while True:
            # 1. print waiting for QR Scan message
            lcd.waiting_message()
            scanned_string = usb_scanner.readQRCode()
            scanned_string = base64.b64decode(scanned_string)

            # take scanned string > check the command (checkin, checkout)
            # if checkin, just directly open the gate, 
            # if checkout, check expired time first before open the gate
            # when checkout and expired time > time_now, print expired message
            json_data = Helper.parse_json_qrcode(scanned_string)
            if json_data['parking_type'] == "checkin":
                mqtt.publish_command(MACHINE_ID, "checkin", json_data)
                # print message selamat datang
                lcd.scan_success_message(gate=0)
                # open gate parking
                print("checkin success")
                gate.open_gate()
            else:
                expired_time = Helper.parse_datetime(json_data['expired'])
                if Helper.parse_to_timestamp(expired_time) > Helper.parse_to_timestamp():
                    # When expired time is more than current time, print expired message
                    lcd.expired_message()
                    print("expired")
                    time.sleep(1)
                    # and continue to first step waiting for QR Scan
                    continue

                lcd.scan_success_message(gate=1)
                mqtt.publish_command(MACHINE_ID, "checkout", json_data)
                print("checkout success")
                gate.open_gate()

            # when vehicle passing the gate, loop to first step
            if ultrasonic.is_vehicle_pass():
                print("vehicle passing the gate")
                gate.close_gate()
            

if __name__ == '__main__':
    main = Main()
