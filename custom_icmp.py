import socket

import pypacker.pypacker as pypacker
from pypacker.pypacker import Packet
from pypacker import ppcap
from pypacker import psocket
from pypacker.layer12 import arp, ethernet, ieee80211, prism
from pypacker.layer3 import ip, icmp
from pypacker.layer4 import udp, tcp


Interface = "wlan0"

try:
    psock = psocket.SocketHndl(iface_name=Interface, timeout=10)
    icmpreq = ethernet.Ethernet(src_s="dc:a6:32:00:a7:8b", dst_s="ec:84:b4:3e:c8:20", type=ethernet.ETH_TYPE_IP) +\
        ip.IP(p=ip.IP_PROTO_ICMP, src_s="192.168.1.35", dst_s="172.217.166.110") +\
        icmp.ICMP(type=8) +\
        icmp.ICMP.Echo(id=1, ts=123456789, body_bytes=b"12345678901234567890")
    psock.send(icmpreq.bin())

    print(icmpreq)

except socket.timeout as e:
    print("timeout!")
except socket.error as e:
    print("you need to be root to execute the raw socket-examples!")
