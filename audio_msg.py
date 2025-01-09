
import os
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
import data


wav_filenames = [
    "chime_big_ben_2-old1.wav",
    "cuckoo_clock1_x.wav",
    "voi_ei_4.wav",
    "sanna_ojoj-old3.wav",
    "sanna_ojoj.wav",
    "onko_ruinattu.wav",
    "chime_big_ben_2.wav",
    "kummeli_tick_8k.wav",
    "uno_dos_tres_16k.wav",
    "bienvenido_8k.wav",
    "bienvenido_16k.wav",
    "diez_nueve_8k.wav",
    "diez_nueve_16k.wav",
    "hastala_proxima_8.wav",
    "hastala_proxima_16k.wav",
    "uno_dos_tres_8k.wav",
    "glockenspiel_munsterplatz_16k.wav",
    "glockenspiel_munsterplatz_22k.wav",
    "solo_en_casa_8k.wav",
    "solo_en_casa_16k.wav" ]    

event_files = {
    data.MODE_START: "uno_dos_tres_8k.wav",
    data.MODE_AT_HOME: "bienvenido_16k.wav",
    data.MODE_COUNT_DOWN:"diez_nueve_8k.wav",
    data.MODE_AWAY: "solo_en_casa_16k.wav",
    data.MODE_WARNING: "cuckoo_clock1_x.wav",
    data.MODE_ALARM: "glockenspiel_munsterplatz_22k.wav",  
    data.MODE_SENDING: "kummeli_tick_8k.wav",
    data.MODE_SET_TIME: "cuckoo_clock1_x.wav",
    data.MODE_12_00: "chime_big_ben_2.wav"
    }




class audio_msg:
    def __init__(self):    
        spi = busio.SPI(gpio.SD_CLK_PIN, gpio.SD_MOSI_PIN, gpio.SD_MISO_PIN)
        cs = digitalio.DigitalInOut(gpio.SD_CS_PIN)
        self.sdcard = adafruit_sdcard.SDCard(spi, cs)
        self.vfs = storage.VfsFat(self.sdcard)
        storage.mount(self.vfs, "/sd")
        self.event = data.MODE_AT_HOME
        try:
            from audioio import AudioOut
        except ImportError:
            try:
                from audiopwmio import PWMAudioOut as AudioOut
                self.audio = AudioOut(gpio.PWM7B_PIN)
            except ImportError:
                pass  # not always supported by every board!
         
    def play_file(self, file_name):
        try:
            with open('/sd/'+file_name, "rb") as f:
                wave = WaveFile(f)
                print("playing", file_name)
                self.audio.play(wave)
                while self.audio.playing:
                    pass
                self.audio.stop()
        except:
            print("Error when playing: ", file_name)
            
    def new_event(self, event):
        if event in event_files:
            self.play_file(event_files[event])
        else:
            print("Event " ,event," was not found")
            
wav_msg = audio_msg();

'''

while 1:
    for file_name in wav_filenames:
        with open('/sd/'+file_name, "rb") as f:
            wave = WaveFile(f)
            print("playing", file_name)
            audio.play(wave)
            while audio.playing:
                pass
            audio.stop()
            time.sleep(2)
'''  