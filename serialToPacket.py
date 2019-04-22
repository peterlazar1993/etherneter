import time
import serial

import pypacker.pypacker as pypacker
from pypacker import psocket
from pypacker.layer12 import ethernet
from pypacker.layer3 import ip, icmp

Interface = "enp0s3"

ser = serial.Serial(
    port='/dev/pts/2',
    baudrate=9600,
)

ser.isOpen()

print('CTRL + C to exit')

val=1
while 1 :
    
    out = ''
    while ser.inWaiting() > 0:
        out = ser.read_until(b'\n')[:-1]
    if out != '':
        try:
            psock = psocket.SocketHndl(iface_name=Interface, timeout=10)
            psock.send(out)

        except socket.timeout as e:
            print("timeout!")
        except socket.error as e:
            print("you need to be root to execute the raw socket-examples!")
        