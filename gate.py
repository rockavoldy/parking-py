from serial import Serial
class Gate:
    """ Initialize Gate
        params: device_path string: path to UART device; default to /dev/ttyAMA0
    """
    def __init__(self, device_path="/dev/ttyAMA0"):
        self.se = Serial(device_path)
        self.se.baudrate = 9600
    
    def open_gate(self):
        print('before open gate')
        self.se.write(b'1')
        print("open gate")

    def close_gate(self):
        print('before close gate')
        self.se.write(b'0')
        print("close gate")
