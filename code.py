import gc
gc.collect()
start_mem = gc.mem_free()
print( "Point 0 Available memory: {} bytes".format(start_mem) ) 

import time

import pico_rtc_u2u_sd_gpio as gpio

#i2c_en = digitalio.DigitalInOut(gpio.EN_I2C_PIN)
#i2c_en.direction = digitalio.Direction.OUTPUT
#i2c_en.value = 1

import xtask
from xtask import Xtask
#import clock24
from clock24 import clock
import color as color
import rtc_pcf8563
import busio
import digitalio
import time

from pico_rtc_u2u_sd_gpio import i2c0
from adafruit_pcf8563.pcf8563 import PCF8563
from rtc_pcf8563 import rtc_pcf8563
from rtc_pcf8563 import rtc
# Storage libraries
import adafruit_sdcard
import storage
import data
from data import date_time
import api
import edog

print()
gc.collect()
start_mem = gc.mem_free()
print( "Point 1 Available memory: {} bytes".format(start_mem) ) 


uart1 = busio.UART(gpio.TX1_PIN, gpio.RX1_PIN, baudrate=9600)
spi = busio.SPI(gpio.SD_CLK_PIN, gpio.SD_MOSI_PIN, gpio.SD_MISO_PIN)
cs = digitalio.DigitalInOut(gpio.SD_CS_PIN)
sdcard = adafruit_sdcard.SDCard(spi, cs)

vfs = storage.VfsFat(sdcard)
# storage.mount(vfs, "/sd")
# rtc = rtc_pcf8563(i2c0)

data.mode['index'] = data.MODE_UNDEFINED

def task_clock24():
    clock.show_time(rtc.date_time.tm_hour, rtc.date_time.tm_min, color.color_arr[color.COLOR_INDX_YELLOW])

def task_rtc():
    rtc.read_time()
    #print(rtc.date_time.tm_hour, rtc.date_time.tm_min)  
    
def task_serial():
    api.read_serial_task()
    
    
    

# define tasks
task_clock_handle = Xtask("Clock24", 0.1, task_clock24)
task_rtc_handle = Xtask("RTC", 5.0, task_rtc)
task_serial_handle = Xtask("Serial", 0.1, task_serial)

tasks = [task_clock_handle,task_rtc_handle, task_serial_handle]
xtask.set_tasks(tasks)

clock.set_time(6,30)
clock.set_mode(data.mode['index'])
print('code:',color.color_arr)

gc.collect()
end_mem = gc.mem_free()

print( "Point 2 Available memory: {} bytes".format(end_mem) )
print( "Code section 1-2 used {} bytes".format(start_mem - end_mem) )

while True:
    xtask.run_tasks()
       
        