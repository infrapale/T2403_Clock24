'''
https://docs.circuitpython.org/en/latest/README.html

---------------------       -------------------- 
| T2401_KeyToRfm    |       | T2403_RelayClock | 
---------------------       -------------------- 
   |                                  |
   |   <C1TS:2023;09;21;19;50>\n      |       set date and time
   |--------------------------------->|
   |                                  |
   |   <C1TG>\n                       |
   |--------------------------------->|       get date and time
   |                                  |
   |   <C1Tg:2023;09;21;19;50>\n      |       reply date and time
   |<---------------------------------|        
   |                                  |
   |                                  |
   |   <C1MSnn>\n                     |       set mode
   |--------------------------------->|
   |                                  |
   |                                  |

'''

import busio
import digitalio
import time
import pico_rtc_u2u_sd_gpio as gpio
import xtask
from micropython import const

CONST_MAX_MSG_LEN = const(32)
# CONST_Y = const(2 * CONST_X + 1)

# uart0 = busio.UART(gpio.TX0_PIN, gpio.RX0_PIN, baudrate=9600, timeout=1)

class UartCom:
    def __init__(self, tx_pin, rx_pin, baudrate ):        
        self.uart = busio.UART(tx_pin, rx_pin, baudrate=baudrate, timeout=10)
        self.msg = ""
        
    def read_msg(self):
        self.msg = ""
        if self.uart.in_waiting > 0: 
            bmsg = self.uart.readline(CONST_MAX_MSG_LEN)
            self.msg = ''.join([chr(b) for b in bmsg]) # convert bytearray to string
        return self.msg

    def send_msg(self, message):
        barr = bytearray(message, 'utf-8')
        self.uart.write(barr)

    def msg_frame_is_ok(self):
        begin = self.msg.find('<')
        end = self.msg.find('>')
        is_ok = False
        if begin >=0 and end > 0:
            self.msg = self.msg[begin+1:end]
            is_ok = True
        return is_ok    
            

ucom = UartCom(gpio.TX0_PIN, gpio.RX0_PIN, 9600)
while 1:
    msg = ucom.read_msg()
    if len(msg) > 0:
        print(msg)
        ucom.send_msg(msg)
        if ucom.msg_frame_is_ok():
            print(ucom.msg)
        else:
            print("Frame error: ",ucom.msg)

while 1:
    if uart0.in_waiting > 0: 
        bmsg = uart0.readline(CONST_MAX_MSG_LEN)
        uart0.write(bmsg);
        msg = ''.join([chr(b) for b in bmsg]) # convert bytearray to string
        print(msg)


