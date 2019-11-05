import machine
from network import WLAN
import time                   # Allows use of time.sleep() for delays
import pycom

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
