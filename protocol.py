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
   |   <C1TR:2023;09;21;19;50>\n      |       reply date and time
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
from uart_com import UartCom
    
    
    
                
'''
<C1TS:123>
<C1TS:2023;09;21;19;50>
<C1TG: >

'''

clock_time = time.struct_time((2024, 3, 21, 19, 50, 0, 3, -1, -1))

def get_date_time_str(d_t):
    return "{};{:02};{:02};{:02};{:02};{:02}".format(
        d_t.tm_year, d_t.tm_mon, d_t.tm_mday, d_t.tm_hour, d_t.tm_min, d_t.tm_sec )
    
 

def cb_set_time():
    global clock_time
    print("cb_set_time")
    str_arr = ucom.parsed['data'].split(';')
    dt = [int(nstr) for nstr in str_arr]
    print(dt)
    clock_time = time.struct_time((dt[0],dt[1],dt[2],dt[3],dt[4],0, 3, -1, -1))
    print(clock_time)

def cb_get_time():
    global clock_time
    print("cb_get_time")
    reply_date_time['data'] = get_date_time_str(clock_time)
    ucom.send_dict_msg(reply_date_time)

cmd_set_time = {'module': 'C', 'index': '1', 'key':'TS', 'data':'', 'cb':cb_set_time}
cmd_get_time = {'module': 'C', 'index': '1', 'key':'TG', 'data':'', 'cb':cb_get_time}

reply_date_time = {'module': 'C', 'index': '1', 'key':'T=', 'data':''}
        
cmds = [cmd_set_time, cmd_get_time]
cmd_tags = ['module','index', 'key']

def check_cmd(rec_msg):
    for cmd in cmds:
        is_match = True
        for tag in cmd_tags:
            if (rec_msg[tag] != cmd[tag]):
                is_match = False
        if is_match:
            cmd['cb']()
            print("Match: ", rec_msg)
            break
            

ucom = UartCom(gpio.TX0_PIN, gpio.RX0_PIN, 9600)
while 1:
    msg = ucom.read_msg()
    if len(msg) > 0:
        print(msg)
        ucom.send_msg(msg)
        if ucom.msg_frame_is_ok():
            print(ucom.msg)
            ucom.parse_msg()
            check_cmd(ucom.parsed)
            print(ucom.parsed)
        else:
            print("Frame error: ",ucom.msg)
        reply_date_time['data']='2023;09;21;19;50'
        ucom.send_dict_msg(reply_date_time)
        



