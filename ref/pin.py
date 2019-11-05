import pycom
import time
from machine import Pin

pycom.heartbeat(False)

push = Pin('P7', mode=Pin.OUT) #G14
buttonIn = Pin('P10', mode=Pin.IN, pull=Pin.PULL_UP) #G17


#print(buttonIn())

while(True):
    if buttonIn():
        push(0)
        print("Push Off")
        time.sleep(1)
    else :
        push(1)
        print("Push On")
        time.sleep(1)
