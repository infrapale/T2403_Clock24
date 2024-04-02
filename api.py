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
import time
import pico_rtc_u2u_sd_gpio as gpio
from micropython import const
from uart_com import UartCom
from clock24 import clock
from rtc_pcf8563 import rtc
    
    
    
                
'''


'''

# clock_time = time.struct_time((2024, 3, 21, 19, 50, 0, 3, -1, -1))

def get_date_time_str(d_t):
    return "{};{:02};{:02};{:02};{:02};{:02}".format(
        d_t.tm_year, d_t.tm_mon, d_t.tm_mday, d_t.tm_hour, d_t.tm_min, d_t.tm_sec )
    
 

def cb_set_time():
    str_arr = ucom.parsed['data'].split(';')
    dt = [int(nstr) for nstr in str_arr]
    # print('dt=',dt)
    dt = time.struct_time((dt[0],dt[1],dt[2],dt[3],dt[4],0, 3, -1, -1))
    rtc.set_time(dt)

def cb_get_time():
    # print("cb_get_time")
    reply_date_time['data'] = rtc.get_time_str()
    ucom.send_dict_msg(reply_date_time)
    
def cb_set_mode():
    # print("cb_set_mode")
    # print(ucom.parsed['data'])
    clock.set_mode(int(ucom.parsed['data']))

def cb_get_mode():
    reply_mode['data'] = data.mode['index']
    ucom.send_dict_msg(reply_mode)

def cb_play_audio():
    pass

cmd_set_time =    {'module': 'C', 'index': '1', 'key':'TS', 'data':'', 'cb':cb_set_time}
cmd_get_time =    {'module': 'C', 'index': '1', 'key':'TG', 'data':'', 'cb':cb_get_time}
reply_date_time = {'module': 'C', 'index': '1', 'key':'T=', 'data':''}
cmd_set_mode =    {'module': 'C', 'index': '1', 'key':'MS', 'data':'', 'cb':cb_set_mode}
reply_mode =      {'module': 'C', 'index': '1', 'key':'MG', 'data':'', 'cb':cb_get_mode}
cmd_play_audio =  {'module': 'C', 'index': '1', 'key':'PA', 'data':'', 'cb':cb_play_audio}

        
cmds = [cmd_set_time, cmd_get_time, cmd_set_mode,cmd_play_audio]
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

def read_serial_task():
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
   

'''
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
        #reply_date_time['data']='2024;04;28;19;50'
        #ucom.send_dict_msg(reply_date_time)
 
 '''




