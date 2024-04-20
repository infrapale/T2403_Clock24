# data module
from micropython import const
import time

MODE_START         = const(0)
MODE_AT_HOME       = const(1)
MODE_COUNT_DOWN    = const(2)
MODE_AWAY          = const(3)
MODE_WARNING       = const(4)
MODE_ALARM         = const(5)
MODE_SENDING       = const(6)

mode = {'index': MODE_START, 'changed':True}
date_time = time.struct_time((2024, 03, 28, 12, 0, 0, 6, -1, -1))

#hms = {'hour':0,'minute':0,'second':0}
#ymd = {'year':0,'month':0,'day':0}