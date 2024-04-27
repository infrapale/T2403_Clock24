# SPDX-FileCopyrightText: 2019 Sommersoft
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

# Simple demo of reading and writing the time for the PCF8563 real-time clock.
# Change the if False to if True below to set the time, otherwise it will just
# print the current date and time every second.  Notice also comments to adjust
# for working with hardware vs. software I2C.
# https://github.com/adafruit/circuitpython/issues/851
# https://learn.adafruit.com/adafruit-wave-shield-audio-shield-for-arduino/convert-files
# https://learn.adafruit.com/mp3-playback-rp2040/pico-mp3
# https://learn.adafruit.com/wave-shield-talking-clock/stuff
# https://docs.circuitpython.org/en/8.2.x/README.html
# https://learn.adafruit.com/adafruit-audio-bff/circuitpython

import audiocore
from audiocore import RawSample
import audiopwmio
import audiobusio
import audiomixer
import time
import board
import busio
import digitalio
import pico_rtc_u2u_sd_gpio as gpio
import array
import math
from adafruit_pcf8563.pcf8563 import PCF8563
import adafruit_sdcard
import storage

from audiocore import WaveFile

# Use any pin that is not taken by SPI

# Connect to the card and mount the filesystem.
#spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
spi = busio.SPI(gpio.SD_CLK_PIN, gpio.SD_MOSI_PIN, gpio.SD_MISO_PIN)
cs = digitalio.DigitalInOut(gpio.SD_CS_PIN)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")



try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        pass  # not always supported by every board!
    
#i2c_en = digitalio.DigitalInOut(gpio.EN_I2C_PIN)
#i2c_en.direction = digitalio.Direction.OUTPUT
#i2c_en.value = 1

# Change to the appropriate I2C clock & data pins here!
#i2c_bus = busio.I2C(gpio.I2C0_SCL_PIN, gpio.I2C0_SDA_PIN, frequency=100000)
#i2c_bus = busio.I2C(board.SCL, board.SDA)

# Create the RTC instance:
rtc = PCF8563(gpio.i2c0)

# Lookup table for names of days (nicer printing).
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


# pylint: disable-msg=using-constant-test
if True:  # change to True if you want to set the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2023, 9, 16, 14, 54, 0, 5, -1, -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    print("Setting time to:", t)  # uncomment for debugging
    rtc.datetime = t
    print()
# pylint: enable-msg=using-constant-test


def open_audio(file_name):
    n = random.choice(wave_files)
    print("playing", n)
    f = open(file_name, "rb")
    w = audiocore.WaveFile(f)
    return f, w

#file_name = "chime_big_ben_2.wav"
file_name = "/sd/chime_big_ben_2.wav"
#file_name = "/sd/cat-time.wav"

with open(file_name, "rb") as f:
    wave = WaveFile(f)
    audio = AudioOut(gpio.PWM7B_PIN)
    print("playing", file_name)
    audio.play(wave)
    while audio.playing:
        pass
    
while 1:
    pass

wave_file = open("chime_big_ben_2.wav", "rb")
wave = WaveFile(wave_file)
audio = AudioOut(board.A0)


# Main loop:
while True:
    if rtc.datetime_compromised:
        print("RTC unset")
    else:
        print("RTC reports time is valid")
    t = rtc.datetime
    print(t)     # uncomment for debugging
    print(
        "The date is {} {}/{}/{}".format(
            days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
        )
    )
    print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
    time.sleep(1)  # wait a second
    
    # Generate one period of sine wav.
    try:
        from audioio import AudioOut
    except ImportError:
        try:
            from audiopwmio import PWMAudioOut as AudioOut
        except ImportError:
            pass  # not always supported by every board!

    button = digitalio.DigitalInOut(board.A1)
    button.switch_to_input(pull=digitalio.Pull.UP)

    while True:
        wave_file = open("chime_big_ben_2.wav", "rb")
        wave = WaveFile(wave_file)

        audio.play(wave)

        # This allows you to do other things while the audio plays!
        t = time.monotonic()
        while audio.playing:
            pass
        #audio.pause()
        print ('ready')
        
        wave_file = open("cuckoo_clock1_x.wav", "rb")
        wave = WaveFile(wave_file)
        audio.play(wave)
        while audio.playing:
            pass

        
        
        
        while time.monotonic() - t < 6:
            pass

        audio.pause()
        print("Waiting for button press to continue!")
        while button.value:
            pass
        audio.resume()
        while audio.playing:
            pass
        print("Done!")
