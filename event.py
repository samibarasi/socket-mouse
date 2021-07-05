#!/usr/bin/python

import struct
import binhex
from signal import signal, SIGINT
from multiprocessing import Process

# You'll need to find the name of your particular mouse to put in here...
file = open("/dev/input/by-path/pci-0000:00:06.0-usb-0:2:1.0-event-mouse","rb")
file2 = open("/dev/input/by-path/pci-0000:00:06.0-usb-0:3:1.0-event-mouse","rb")

def handler(signal_received, frame):
    global run_code
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    run_code = False

def read(file, num):
    while 1:
        byte = file.read(16)
    #    h = ":".join("{:02x}".format(ord(c)) for c in byte)
    #    print "byte=",h

        (type,code,value) =  struct.unpack_from('hhi', byte, offset=8)

        if type == 1 and value == 1:
            if code == 272:
                print(num, "LEFT PRESS")
            if code == 273:
                print(num, "RIGHT PRESS")

        if type == 2:
            if code == 0:
                print(num, "MOVE L/R",value)
            if code == 1:
                print(num, "MOVE U/D",value)


if __name__ == '__main__':
    run_code = True
    signal(SIGINT, handler)
    program1 = Process(target=read, args=(file, 1))
    program1.start()
    program2 = Process(target=read, args=(file2, 2))
    program2.start()

    while run_code:
       pass

    program1.terminate()
    program2.terminate()
