import socket

import pypacker.pypacker as pypacker
from pypacker.pypacker import Packet
from pypacker import ppcap
from pypacker import psocket
from pypacker.layer12 import arp, ethernet, ieee80211, prism
from pypacker.layer3 import ip, icmp
from pypacker.layer4 import udp, tcp


Interface = "enp0s3"

try:
    psock = psocket.SocketHndl(iface_name=Interface, timeout=10)
    icmpreq = ethernet.Ethernet(src_s="a4:5e:60:db:f3:3f", dst_s="28:6c:07:c3:f0:53", type=ethernet.ETH_TYPE_IP) +\
        ip.IP(p=ip.IP_PROTO_ICMP, src_s="192.168.31.57", dst_s="216.58.197.46") +\
        icmp.ICMP(type=8) +\
        icmp.ICMP.Echo(id=1, ts=123456789, body_bytes=b"12345678901234567890")
    psock.send(icmpreq.bin())

except socket.timeout as e:
    print("timeout!")
except socket.error as e:
    print("you need to be root to execute the raw socket-examples!")
