# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 03:52:24 2017

@author: Frank
"""

import socket

if __name__ == "__main__":
    sock = socket.socket()
    sock.connect(("localhost", 50839))

    with open("data.bin", "rb") as fd:
        buf = fd.read(1024)
        while (buf):
            sock.send(buf)
            buf = fd.read(1024)
    sock.close()