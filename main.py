import optparse
import socket
import time
import binascii
import pypacker.pypacker as pypacker
from pypacker.pypacker import Packet
from pypacker import ppcap
from pypacker import psocket
from pypacker.layer12 import arp, ethernet, ieee80211, prism
from pypacker.layer3 import ip, icmp
from pypacker.layer4 import udp, tcp


print("Test")

BUF_SIZE = 1600		# > 1500

ETH_P_ALL = 3		# To receive all Ethernet protocols

# Interface = "eth0"
Interface = "wlan0"

host = socket.gethostbyname(socket.gethostname())


### Packet handler ###

def printPacket(packet, now, message):
    newPacket = ethernet.Ethernet(packet)
    if newPacket.dst_s != '<current device MAC in capitals>' or newPacket.dst_s != 'FF:FF:FF:FF:FF:FF':
        print('---------------')
        print(newPacket)
    # print(message, len(packet), "bytes  time:", now,
    #       "\n  SMAC:", SMAC(packet), " DMAC:", DMAC(packet),
    #       " Type:", EtherType(packet), "\n  Payload:", Payload(packet))  # !! Python 3 !!


def terminal():
    # Parse command line
    parser = optparse.OptionParser()
    parser.add_option("--p", "--port", dest="port", type="int",
                      help="Local network port id")
    parser.add_option("--lm", "--lmac", "--localMAC", dest="lmac", type="str",
                      help="Local MAC address")
    parser.add_option("--rm", "--rmac", "--remoteMAC", dest="rmac", type="str",
                      help="Remote MAC address")
    parser.add_option("--receiveOnly", "--receiveonly",
                      dest="receiveOnly", action="store_true")
    # parser.add_option("--promiscuous", dest = "promiscuous", action = "store_true")
    parser.set_defaults(lmac="ffffffffffff", rmac="ffffffffffff")
    opts, args = parser.parse_args()

    # Open socket
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW,
                         socket.htons(ETH_P_ALL))
    sock.bind((Interface, ETH_P_ALL))
    sock.setblocking(0)

    # Contents of packet to send (constant)
    sendPacket = binascii.unhexlify(opts.rmac) + binascii.unhexlify(opts.lmac) + \
        b'\x88\xb5' + b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'

    # Repeat sending and receiving packets
    interval = 1
    lastTime = time.time()
    while True:
        now = time.time()

        try:
            packet = sock.recv(BUF_SIZE)
        except socket.error:
            pass
        else:
            printPacket(packet, now, "Received:")

        if not opts.receiveOnly:
            if now > lastTime + interval:
                sendBytes = sock.send(sendPacket)
                printPacket(sendPacket, now, "Sent:   ")
                lastTime = now
            else:
                time.sleep(0.001001)
        else:
            time.sleep(0.001001)


terminal()
