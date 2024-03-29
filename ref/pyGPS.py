#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

import machine
import math
import network
import os
import time
import utime
import gc
from machine import RTC
from machine import SD
from L76GNSS import L76GNSS
from pytrack import Pytrack

#ACC exam
from LIS2HH12 import LIS2HH12

time.sleep(2)
gc.enable()

# setup rtc
rtc = machine.RTC()
rtc.ntp_sync("pool.ntp.org")
utime.sleep_ms(750)
print('\nRTC Set from NTP to UTC:', rtc.now())
utime.timezone(7200)
print('Adjusted from UTC to EST timezone', utime.localtime(), '\n')

py = Pytrack()
l76 = L76GNSS(py, timeout=30)

#ACC exam
acc = LIS2HH12()

sd = SD()
os.mount(sd, '/sd')


while (True):
    coord = l76.coordinates()

    #SD Write
    f = open('/sd/gps-record_04.txt', 'a')
    f.write("{} - {}\n".format(coord, rtc.now()))
    f.close()

    print("{} - {} - {}".format(coord, rtc.now(), gc.mem_free()))

    #Acc exam
    pitch = acc.pitch()
    roll = acc.roll()
    print('{},{}'.format(pitch,roll))
    time.sleep_ms(100)
