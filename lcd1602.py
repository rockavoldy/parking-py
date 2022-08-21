# -*- coding: utf-8 -*-

import i2clcd
import time


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
            if message below 16 characters, print message as static
            if message above 16 characters, print message as running text
            params msg str: message to be printed 
            return bool: True if success else False 
        """
        if not msg:
            return False

        self._lcd.clear()
        if len(msg) < 16:
            self._lcd.print_line(msg, 0)
            return True

        self._lcd.shift(direction='LEFT', move_display=False)
        self._lcd.print(msg)
        # add delay, easier to read
        time.sleep(0.13)

        return True

    def waiting_message(self):
        """ Waiting for scanner to found the QR Code """
        self.print_message("Silahkan scan QR Code anda!")
    
    def scan_success_message(self, gate=0):
        """ Scan success message
            params: gate bool: 0 for gate entry, 1 for gate exit
        """
        if gate == 0:
            self.print_message("Selamat datang!")
        else:
            self.print_message("Terima kasih atas kunjungan anda!")

    def expired_message(self):
        """ Expired message """
        self.print_message("Waktu pembayaran anda telah habis!, Silahkan ikuti instruksi di HP anda!")

    def recheckin_message(self):
        self.print_message("Silahkan ikuti instruksi di HP anda!")

    def invalid_qr_message(self):
        self.print_message("QR Code anda invalid, silahkan generate kembali!")

    def waiting_payment_message(self):
        """ Waiting for Payment message """
        self.print_message("Silahkan lakukan pembayaran dengan QRIS yang telah kami kirimkan!")