# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 03:52:54 2017

@author: Frank
"""

import sys
import socket

if __name__ == "__main__":
    sock = socket.socket()
    sock.bind(("localhost", 50839))
    sock.listen(1)

    client, address = sock.accept()

    buf = client.recv(1024)
    while (buf):
        sys.stdout.write(buf)
        buf = client.recv(1024)

    client.close()
    sock.close()