# -*- coding: utf-8 -*-

import i2clcd


class LCD1602():
    """ Initialize LCD1602
        params i2c_bus int: i2c bus used; default to 1 
        params i2c_addr hexadecimal: address for lcd1602; default to 0x27; 
                                     CHANGE THIS if you have more than one lcd connected on the same i2cbus 
    """
    def __init__(self, i2c_bus=1, i2c_addr=0x27):
        self._lcd = i2clcd.i2clcd(i2c_bus=i2c_bus, i2c_addr=i2c_addr, lcd_width=16)
        self._lcd.init()

    def print_message(self, msg=None) -> bool:
        """ Print message to the LCD
            params msg str: message to be printed 
            return bool: True if success else False 
        """
        if not msg:
            return False
        
        # TODO: validate the length of message; make sure it fit. 
        # When the message can't fit the width of lcd, make the message rolling on that line only
        self._lcd.print_line(msg, line=0)

        return True

    def waiting_message(self):
        """ Waiting for scanner to found the QR Code """
        self.print_message("Silahkan scan QR Code anda!")
    
    def scan_success_message(self, gate=0):
        """ Scan success message
            params: gate bool: 0 for gate entry, 1 for gate exit
         """
         # TODO: make this customizable, for the gate entry and gate exit
        self.print_message("Terima kasih")

    def waiting_payment_message(self):
        """ Waiting for Payment message """
        self.print_message("Silahkan lakukan pembayaran dengan QRIS yang telah kami kirimkan!")