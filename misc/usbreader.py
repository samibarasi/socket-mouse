#!/usr/bin/python

import struct
import os
import time, datetime
from signal import signal, SIGINT
from multiprocessing import Process

seconds_duration = 5

def helperFunc(item):
    #print(item)
    return True if item.startswith("mouse2") else False

def handler(signal_received, frame):
    global run_code
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    run_code = False

def Main(filename):
    file = open(filename,"rb")
    print("reading file {}".format(filename))
    while True:
            
        byte = file.read(16)
        h = ":".join("{:02x}".format(ord(c)) for c in byte)
        print ("byte=", h)

        (type,code,value) =  struct.unpack_from('hhi', byte, offset=8)

        print(type, code, value)
        if type == 1 and value == 1:
            if code == 272:
                print("LEFT PRESS")
            if code == 273:
                print("RIGHT PRESS")

        if type == 2:
            if code == 0:
                print("MOVE L/R",value)
            if code == 1:
                print("MOVE U/D",value)
       
if __name__ == '__main__':
    run_code = True
    files = list(filter(helperFunc, os.listdir("/dev/input")))

    now = datetime.datetime.now()
    finish_time = now + datetime.timedelta(seconds=seconds_duration)
        # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)
    filename = "/dev/input/{}".format(files.pop(0))
    program = Process(target=Main, args=(filename,))
    program.start()
    while run_code:
        now = datetime.datetime.now()
        if now > finish_time:
            program.terminate()
            if not len(files):
                print("done.")
                exit(0)
                
            filename = "/dev/input/{}".format(files.pop(0))
            program = Process(target=Main, args=(filename,))
            program.start()
            finish_time = now + datetime.timedelta(seconds=seconds_duration)
            print("remaining {}".format(len(files)))

    # Clean up
    program.terminate()
    



