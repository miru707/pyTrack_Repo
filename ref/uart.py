from machine import UART
import pycom
import time

# this uses the UART_1 non-default pins for TXD and RXD (``P20`` and ``P21``)
uart = UART(1, baudrate=9600, pins=('P10','P9'))

pycom.heartbeat(False)

uart.write('C,1\r')

while(True):

    # read up to 5 bytes
    time.sleep(1)

    time.sleep(0.5)
    print(uart.read(5))
