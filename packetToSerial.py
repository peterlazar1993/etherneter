import time
import serial

import pypacker.pypacker as pypacker
from pypacker import psocket
from pypacker.layer12 import ethernet
from pypacker.layer3 import ip, icmp

ser = serial.Serial(
    port='/dev/pts/1',
    baudrate=9600
)

print('Enter your commands below.\r\nInsert "exit" to leave the application.')

val=1
while 1 :
    
    val = input(">> ")
    if val == 'exit':
        ser.close()
        exit()
    else:
        icmpreq = ethernet.Ethernet(src_s="a4:5e:60:db:f3:3f", dst_s="e4:6f:13:c0:36:81", type=ethernet.ETH_TYPE_IP) +\
            ip.IP(p=ip.IP_PROTO_ICMP, src_s="192.168.1.7", dst_s="216.58.197.46") +\
            icmp.ICMP(type=8) +\
            icmp.ICMP.Echo(id=1, ts=123456789,
                           body_bytes=b"12345678901234567890")
        ser.write(icmpreq.bin()+b'\n')