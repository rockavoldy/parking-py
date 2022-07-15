from usbscanner import USBScanner
from lcd1602 import LCD1602
from ultrasonic import Ultrasonic
from mqtt import Mqtt

class Main():
    def __init__(self):
        lcd = LCD1602()
        # ultrasonic = Ultrasonic(echo_pin=17, trigger_pin=27)
        # device_path = "/dev/input/event0"
        # usb_scanner = USBScanner(device_path)
        # lcd.waiting_message()
        # scanned_string = usb_scanner.readQRCode()
        # if scanned_string != None:
        while True:
            # usb_scanner.device.ungrab()
            # print(scanned_string)
            lcd.scan_success_message()
            # distance = ultrasonic.distance()
            # print(distance)
        else:
            lcd.waiting_payment_message()

main = Main()

class Display():
    def __init__(self):
        lcd = LCD1602()
        mqtt = Mqtt()

        while True:
            lcd.waiting_message()
            # TODO: add scanner to check if found mqtt command that says to change the message
            # when command to change the message found, change the message, 
            # and send command to open gate or scan QR
    
    def check_command(self):
