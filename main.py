from usbscanner import USBScanner
from lcd1602 import LCD1602
from ultrasonic import Ultrasonic

class Main():
    def __init__(self):
        # lcd = LCD1602()
        ultrasonic = Ultrasonic(echo_pin=17, trigger_pin=27)
        # device_path = "/dev/input/event0"
        # usb_scanner = USBScanner(device_path)
        # lcd.waiting_message()
        # scanned_string = usb_scanner.readQRCode()
        # if scanned_string != None:
        while True:
            # usb_scanner.device.ungrab()
            # print(scanned_string)
            # lcd.scan_success_message()
            distance = ultrasonic.distance()
            print(distance)
        # else:
        #     lcd.waiting_payment_message()

main = Main()