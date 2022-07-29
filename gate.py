import serial

class Gate:
    """ Initialize Gate
        params: device_path string: path to UART device; default to /dev/ttyAMA0
    """
    def __init__(self, device_path="/dev/ttyAMA0"):
        self.se = serial.Serial(device_path)
        self.se.baudrate = 9600
    
    def open_gate(self):
        self.se.write(1)

    def close_gate(self):
        self.se.write(0)