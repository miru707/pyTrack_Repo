import machine
import math
import network
import os
import time
import utime
import gc #Enable automatic garbage collection.
import pycom
import json

from machine import RTC
from machine import SD
from network import WLAN
#EC Sensor communication
from machine import UART
#GPS
from L76GNSS import L76GNSS
from pytrack import Pytrack

time.sleep(1)
gc.enable()

#SD card mount
sd = SD()
os.mount(sd, '/sd')

# this uses the UART_1 non-default pins for TXD and RXD (``P9`` and ``P10``)
uart = UART(1, baudrate=9600, pins=('P10','P9'))

# Wireless network
# WIFI_SSID = "KT_GIGA_2G_1105"
# WIFI_PASS = "jangkiho558519" # No this is not our regular password. :)
# WIFI_IP = '172.30.1.88'
# WIFI_GATE = '172.30.1.254'
# WIFI_DNS = '168.126.63.1'

WIFI_SSID = "jincontrols"
WIFI_PASS = "jincontrols2016" # No this is not our regular password. :)
WIFI_IP = '192.168.0.88'
WIFI_GATE = '192.168.0.1'
WIFI_DNS = '168.126.63.1'


pycom.heartbeat(False)
time.sleep(0.1) # Workaround for a bug.
                # Above line is not actioned if another
                # process occurs immediately afterwards
pycom.rgbled(0xff0000)  # Status red = not working


# configure the WLAN subsystem in station mode (the default is AP)
wlan = WLAN(mode=WLAN.STA)
# go for fixed IP settings (IP, Subnet, Gateway, DNS)
wlan.ifconfig(config=(WIFI_IP, '255.255.255.0', WIFI_GATE, WIFI_DNS))
wlan.scan()     # scan for available networks
wlan.connect(ssid=WIFI_SSID, auth=(WLAN.WPA2, WIFI_PASS))

print("\nConnected to Wifi\n")


# pycom.rgbled(0xffd7000) # Status orange: partially working
pycom.rgbled(0x000022)# Status blue: stopped

while not wlan.isconnected():
    pass

print(wlan.ifconfig())

#SD Write ifconfig
f = open('/sd/log_wifi_config.txt', 'a')
f.write("{}".format(wlan.ifconfig()))
f.close()

pycom.heartbeat(True)

print("OK\n")

# setup rtc
rtc = machine.RTC()
rtc.ntp_sync("pool.ntp.org")
utime.sleep_ms(750)
print('RTC Set from NTP to UTC:', rtc.now())
utime.timezone(32400) # 60sec*60min*9Hour = 32400 sec
print('Adjusted from UTC to EST timezone', utime.localtime(), '\n')

loTime = utime.localtime()
yearLT = loTime[0]
monLT = loTime[1]
monLT = "{0:0>2}".format(monLT)
dayLT = str(loTime[2])
dayLT = "{0:0>2}".format(dayLT)
hourLT = loTime[3]
hourLT = "{0:0>2}".format(hourLT)
minLT = loTime[4]
minLT = "{0:0>2}".format(minLT)
print("{}-{}-{}-{}-{}".format(yearLT,monLT,dayLT,hourLT,minLT))

dateDir = "/sd/" + str(yearLT) + str(monLT) + str(dayLT)
dateFull = str(yearLT) + str(monLT) + str(dayLT) + str(hourLT)
print(dateDir,'\n')

#directory path create
try:
    os.listdir(dateDir)
    print("directory Exists!!",'\n')
except:
    os.mkdir(dateDir)

#filename  create
fullpath = dateDir + "/test_" + dateFull + ".txt"

f = open(fullpath,'a')
f.write("data save time : " + str(loTime))
f.write("\n")
f.close()

#sensor write value
uart.write('C,60\r')
time.sleep(1)
print(uart.readall())

while(True):

    # read up to 5 bytes

    EcData=str(uart.read(5))
    EData = EcData[2:6]
    print(EData)

#    loTime = str(utime.localtime())
    loTime = utime.localtime()
    yearLT = loTime[0]
    monLT = loTime[1]
    monLT = "{0:0>2}".format(monLT)
    dayLT = str(loTime[2])
    dayLT = "{0:0>2}".format(dayLT)
    hourLT = loTime[3]
    hourLT = "{0:0>2}".format(hourLT)
    minLT = loTime[4]
    minLT = "{0:0>2}".format(minLT)
    secLT = loTime[5]
    secLT = "{0:0>2}".format(secLT)

    dateDir = "/sd/"+str(yearLT)+str(monLT)+str(dayLT)
    dateFileNa = str(yearLT)+str(monLT)+str(dayLT)+str(hourLT)
    dateFull = str(yearLT)+str(monLT)+str(dayLT)+str(hourLT)+str(minLT)+str(secLT)
    print(dateFull)

    fullpath = dateDir + "/" + dateFileNa + ".txt"
    print(fullpath)

    f = open(fullpath,'a')
    f.write("Time:" + dateFull + ", EC:" + EData)
    f.write("\n")
    f.close()
    time.sleep(60)
