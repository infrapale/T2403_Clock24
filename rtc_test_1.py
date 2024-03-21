import busio
import digitalio
import pico_rtc_u2u_sd_gpio as gpio
import time
from adafruit_pcf8563.pcf8563 import PCF8563
# import rtc_pcf8563
from rtc_pcf8563 import rtc_pcf8563

# Storage libraries
import adafruit_sdcard
import storage

# Power on I2C
i2c_en = digitalio.DigitalInOut(gpio.EN_I2C_PIN)
i2c_en.direction = digitalio.Direction.OUTPUT
i2c_en.value = 1

uart1 = busio.UART(gpio.TX1_PIN, gpio.RX1_PIN, baudrate=9600)
spi = busio.SPI(gpio.SD_CLK_PIN, gpio.SD_MOSI_PIN, gpio.SD_MISO_PIN)
cs = digitalio.DigitalInOut(gpio.SD_CS_PIN)
sdcard = adafruit_sdcard.SDCard(spi, cs)
i2c0 = busio.I2C(gpio.I2C0_SCL_PIN, gpio.I2C0_SDA_PIN, frequency=100000)

# Change to the appropriate I2C clock & data pins here!
# i2c_bus = busio.I2C(gpio.I2C0_SCL_PIN, gpio.I2C0_SDA_PIN, frequency=100000)
i2c1 = busio.I2C(gpio.I2C1_SCL_PIN, gpio.I2C1_SDA_PIN, frequency=1000000)

vfs = storage.VfsFat(sdcard)
# storage.mount(vfs, "/sd")
rtc = rtc_pcf8563(i2c0)

# Main loop:
while True:
    rtc.print_time()
    time.sleep(1)  # wait a second
