import time
import serial
import sys
import socket
import threading

import pypacker.pypacker as pypacker
from pypacker import psocket
from pypacker.layer12 import ethernet
from pypacker.layer3 import ip, icmp

Interface = "eth0"


class Etherneter:
    def __init__(self, serial_instance, socket):
        self.serial = serial_instance
        self.socket = socket
        self._write_lock = threading.Lock()

    def run(self):
        self.alive = True
        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.daemon = True
        self.thread_read.name = 'serial->socket'
        self.thread_read.start()
        self.thread_write = threading.Thread(target=self.writer)
        self.thread_write.daemon = True
        self.thread_write.name = 'socket->serial'
        self.thread_write.start()

    def reader(self):
        """loop forever and copy serial->socket"""
        while self.alive:
            try:
                data = self.serial.read_until(b'\n')[:-1]
                if data:
                    self.write(data)
            except socket.error as msg:
                break
        self.alive = False

    def write(self, data):
        """thread safe socket write with no data escaping. used to send telnet stuff"""
        with self._write_lock:
            self.socket.send(data)

    def writer(self):
        """loop forever and copy socket->serial"""
        while self.alive:
            try:
                data = self.socket.recv()
                print(ethernet.Ethernet(data))
                if not data:
                    break
                self.serial.write(data+b'\n')
            except socket.error as msg:
                # probably got disconnected
                break
        self.stop()

    def stop(self):
        """Stop copying"""
        if self.alive:
            self.alive = False
            self.thread_read.join()
            self.thread_write.join()


if __name__ == '__main__':

    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = '/dev/ttyS0'

    psock = None

    try:
        ser.open()
    except serial.SerialException as e:
        sys.exit(1)

    try:
        psock = psocket.SocketHndl(iface_name=Interface, timeout=10)
    except socket.error as msg:
        sys.exit(1)

    try:
        e = Etherneter(ser, psock)
        try:
            e.run()
        finally:
            e.stop()
            psock.close()
    except KeyboardInterrupt:
        sys.stdout.write('\n')
