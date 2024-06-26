#----------------------------------------------------------
# clock24.py
#
#----------------------------------------------------------
from micropython import const
import time
import pico_rtc_u2u_sd_gpio as gpio
import board
from rainbowio import colorwheel
import neopixel
import color as color
import data


# print ('clock24',color.color_arr)

NUMPIXELS = 24  # Update this to match the number of LEDs.
SPEED = 0.05  # Increase to slow down the rainbow. Decrease to speed it up.
BRIGHTNESS = 0.2  # A number between 0.0 and 1.0, where 0.0 is off, and 1.0 is max.


pixels = neopixel.NeoPixel(gpio.RGB1_PIN, NUMPIXELS, brightness=BRIGHTNESS, auto_write=False)       

class Spinner:
    def __init__(self, c_indx, spin_dir, spin_wait,spin_pos, spin_active):
        self.color_indx = c_indx 
        self.direction = spin_dir
        self.wait = spin_wait
        self.pos = spin_pos
        self.cntr = 0
        self.active = spin_active
        
    def next_pos(self):
        self.cntr = self.cntr + 1
        if self.cntr > self.wait:
            self.cntr = 0
            self.pos = self.pos + self.direction
            if self.pos > 23:
                self.pos = 0
            if self.pos < 0:
                self.pos = 23
    def activate(self, spin_active):
        self.active = spin_active

class Clock24:
    HOURS_PER_DAY = const(24)
    MINUTES_PER_HOUR = const(60)
    HALF_DAY_MINUTES = const(12*MINUTES_PER_HOUR)
    FULL_DAY_MINUTES = const(24*MINUTES_PER_HOUR)
    

    def __init__(self):
        self.mode = data.MODE_START
        self.hour = 0
        self.minute = 0
        self.rot1 = 0
        self.rot2 = 23
        self.hour_minutes = [0]*(HOURS_PER_DAY+1)
        for h in range(HOURS_PER_DAY+1):
            self.hour_minutes[h] = h * MINUTES_PER_HOUR
        self.spinner0 = Spinner(color.COLOR_INDX_BLUE,1,0,6, True)
        self.spinner1 = Spinner(color.COLOR_INDX_YELLOW,-1,2,12, True)
        self.spinner2 = Spinner(color.COLOR_INDX_RED,-1,1,18, True)
        self.spinner3 = Spinner(color.COLOR_INDX_WHITE,-1,1,20, True)
        self.spinners = [self.spinner0, self.spinner1, self.spinner2, self.spinner3]
        self.spinner2.activate(False)
        self.spinner3.activate(False)
        # print(self.hour_minutes)
        
    def set_time(self,h,m):
        self.hour = h
        self.minute = m

    def minute_distance(self,hour, minute, scale_hour):
        minutes_now = self.hour_minutes[hour] + minute
        minutes_scale = self.hour_minutes[scale_hour]
        dist = abs(minutes_now - minutes_scale)
        if (minutes_scale >  minutes_now ):
            if((minutes_now < HALF_DAY_MINUTES) and (minutes_scale > HALF_DAY_MINUTES)):
                dist = minutes_now + (FULL_DAY_MINUTES - minutes_scale)
        else:
            if((minutes_now > HALF_DAY_MINUTES) and (minutes_scale < HALF_DAY_MINUTES)):
                dist = minutes_scale + (FULL_DAY_MINUTES - minutes_now)
        return abs(dist)
    
    def show_time(self, h, m, needle_color):
        for scale_h in range(24):
            distance = self.minute_distance(h,m,scale_h)
            mult = 0
            if  distance < 31:
                mult = 1.0
            elif distance < 80:
                mult = 0.05
            c_mult = (mult, mult, mult)    
            ncolor = tuple( int(c*m) for c, m in zip(needle_color,c_mult))  
            
            # print(h,m,scale_h,distance, red)
            pixels[scale_h] = ncolor
            # colorwheel(pixel_index & 255)
            for spin in self.spinners:
                if spin.active and (spin.pos == scale_h):
                    pixels[scale_h] = color.color_arr[spin.color_indx]
                    
        for spin in self.spinners:
            spin.next_pos()    
            
        pixels.show()
    def set_mode(self, new_mode):
        if new_mode != self.mode:
            self.mode = new_mode

            for spin in self.spinners:
                spin.active = False
                spin.direction = 1
                spin.wait = 0
                spin.pos = 0

            if self.mode == data.MODE_START:
                self.spinner0.color_indx = color.COLOR_INDX_RED
                self.spinner0.pos = 6
                self.spinner0.active = True

                self.spinner1.color_indx = color.COLOR_INDX_GREEN
                self.spinner1.pos = 4
                self.spinner1.active = True
                
            elif self.mode == data.MODE_AT_HOME:
                self.spinner0.color_indx = color.COLOR_INDX_GREEN
                self.spinner0.pos = 6
                self.spinner0.active = True

                self.spinner1.color_indx = color.COLOR_INDX_GREEN
                self.spinner1.pos = 5
                self.spinner1.active = True
            
            elif self.mode == data.MODE_COUNT_DOWN:
                self.spinner0.color_indx = color.COLOR_INDX_GREEN
                self.spinner0.pos = 6
                self.spinner0.wait = 0
                self.spinner0.active = True

                self.spinner1.color_indx = color.COLOR_INDX_RED
                self.spinner1.pos = 7
                self.spinner1.direction = 1
                self.spinner1.wait = 0
                self.spinner1.active = True

                self.spinner2.color_indx = color.COLOR_INDX_BLUE
                self.spinner2.pos = 8
                self.spinner2.wait = 0
                self.spinner2.active = True

                self.spinner3.color_indx = color.COLOR_INDX_WHITE
                self.spinner3.pos = 9
                self.spinner3.wait = 0
                self.spinner3.direction = 1
                self.spinner3.active = True
                
            elif self.mode == data.MODE_AWAY:
                self.spinner0.color_indx = color.COLOR_INDX_RED
                self.spinner0.pos = 6
                self.spinner0.wait = 0
                self.spinner0.active = True

                self.spinner1.color_indx = color.COLOR_INDX_RED
                self.spinner1.pos = 18
                self.spinner1.wait = 0
                self.spinner1.active = True

                self.spinner2.color_indx = color.COLOR_INDX_RED
                self.spinner2.pos = 6
                self.spinner2.wait = 0
                self.spinner2.direction = -1
                self.spinner2.active = True

                self.spinner3.color_indx = color.COLOR_INDX_RED
                self.spinner3.pos = 18
                self.spinner3.wait = 0
                self.spinner3.direction = -1
                self.spinner3.active = True

            elif self.mode == data.MODE_WARNING:
                self.spinner0.color_indx = color.COLOR_INDX_RED
                self.spinner0.pos = 6
                self.spinner0.wait = 0
                self.spinner0.active = True

                self.spinner1.color_indx = color.COLOR_INDX_RED
                self.spinner1.pos = 12
                self.spinner1.wait = 0
                self.spinner1.active = True

                self.spinner2.color_indx = color.COLOR_INDX_RED
                self.spinner2.pos = 18
                self.spinner2.wait = 0
                self.spinner2.direction = 1
                self.spinner2.active = True

                self.spinner3.color_indx = color.COLOR_INDX_RED
                self.spinner3.pos = 0
                self.spinner3.wait = 0
                self.spinner3.direction = 1
                self.spinner3.active = True

            elif self.mode == data.MODE_ALARM:
                self.spinner0.color_indx = color.COLOR_INDX_RED
                self.spinner0.pos = 6
                self.spinner0.wait = 0
                self.spinner0.active = True

                self.spinner1.color_indx = color.COLOR_INDX_RED
                self.spinner1.pos = 7
                self.spinner1.wait = 0
                self.spinner1.active = True

                self.spinner2.color_indx = color.COLOR_INDX_RED
                self.spinner2.pos = 6
                self.spinner2.wait = 0
                self.spinner2.direction = -1
                self.spinner2.active = True

                self.spinner3.color_indx = color.COLOR_INDX_RED
                self.spinner3.pos = 7
                self.spinner3.wait = 0
                self.spinner3.direction = -1
                self.spinner3.active = True

            elif self.mode == data.MODE_SENDING:
                self.spinner0.color_indx = color.COLOR_INDX_BLUE
                self.spinner0.pos = 6
                self.spinner0.active = True

                self.spinner1.color_indx = color.COLOR_INDX_BLUE
                self.spinner1.pos = 8
                self.spinner1.active = True

                self.spinner2.color_indx = color.COLOR_INDX_BLUE
                self.spinner2.pos = 10
                self.spinner2.active = True

                self.spinner3.color_indx = color.COLOR_INDX_BLUE
                self.spinner3.pos = 12
                self.spinner3.active = True

clock = Clock24()
            
'''        
clock = Clock24()

def test_main():
    global clock
    print(clock.HOURS_PER_DAY)
    clock.set_time(6,30)
    test_minutes = [ i*10 for i in range(6)]
    clock.set_mode(MODE_COUNT_DOWN)
    while True:
        for h in range(24):
            for m in test_minutes:
                clock.show_time(h,m, color.color_arr[color.COLOR_INDX_YELLOW])
                time.sleep(0.1)
# test_main()
'''
