from usbscanner import USBScanner
from lcd1602 import LCD1602
from ultrasonic import Ultrasonic
from mqtt import Mqtt
from gate import Gate

class Main():
    def __init__(self):
        lcd = LCD1602()
        ultrasonic = Ultrasonic(echo_pin=17, trigger_pin=27)
        # NOTE: path to USB device when it's already plugged will be at /dev/input/event0
        # if it plugged after raspi up, it will be at /dev/input/event1
        device_path = "/dev/input/event1"
        usb_scanner = USBScanner(device_path)
        # Gate take device_path too, but since it's only 1 device_path
        # i think it's ok to use the default one /dev/ttyAMA0
        gate = Gate()
        while True:
            # 1. print waiting for QR Scan message
            lcd.waiting_message()
            # 2. read QR Code
            scanned_string = usb_scanner.readQRCode()
            print(scanned_string)
            # 3. TODO: publish data to mqtt topic
            # 4. print message selamat datang
            lcd.scan_success_message()
            # 5. TODO: open gate parking
            gate.open_gate()
            # 6. activate ultrasonic to scan if vehicle is already passing the gate
            # 7. when vehicle passing the gate, loop to first step
            if is_vehicle_pass():
                gate.close_gate()
            

if __name__ == '__main__':
    main = Main()
