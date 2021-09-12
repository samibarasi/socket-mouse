#!/usr/bin/env python3

import socket
import os
from dotenv import load_dotenv
from pynput import mouse
from signal import signal, SIGINT
from multiprocessing import Process
from pprint import pprint

load_dotenv()

width, height = 2560, 1440
MAX = 10000

from ctypes import *
from ctypes.wintypes import *

#Constants

#For touchMask
TOUCH_MASK_NONE=          0x00000000 #Default
TOUCH_MASK_CONTACTAREA=   0x00000001
TOUCH_MASK_ORIENTATION=   0x00000002
TOUCH_MASK_PRESSURE=      0x00000004
TOUCH_MASK_ALL=           0x00000007

#For touchFlag
TOUCH_FLAG_NONE=          0x00000000

#For pointerType
PT_POINTER=               0x00000001#All
PT_TOUCH=                 0x00000002
PT_PEN=                   0x00000003
PT_MOUSE=                 0x00000004

#For pointerFlags
POINTER_FLAG_NONE=        0x00000000#Default
POINTER_FLAG_NEW=         0x00000001
POINTER_FLAG_INRANGE=     0x00000002
POINTER_FLAG_INCONTACT=   0x00000004
POINTER_FLAG_FIRSTBUTTON= 0x00000010
POINTER_FLAG_SECONDBUTTON=0x00000020
POINTER_FLAG_THIRDBUTTON= 0x00000040
POINTER_FLAG_FOURTHBUTTON=0x00000080
POINTER_FLAG_FIFTHBUTTON= 0x00000100
POINTER_FLAG_PRIMARY=     0x00002000
POINTER_FLAG_CONFIDENCE=  0x00004000
POINTER_FLAG_CANCELED=    0x00008000
POINTER_FLAG_DOWN=        0x00010000
POINTER_FLAG_UPDATE=      0x00020000
POINTER_FLAG_UP=          0x00040000
POINTER_FLAG_WHEEL=       0x00080000
POINTER_FLAG_HWHEEL=      0x00100000
POINTER_FLAG_CAPTURECHANGED=0x00200000


#Structs Needed

class POINTER_INFO(Structure):
    _fields_=[("pointerType",c_uint32),
              ("pointerId",c_uint32),
              ("frameId",c_uint32),
              ("pointerFlags",c_int),
              ("sourceDevice",HANDLE),
              ("hwndTarget",HWND),
              ("ptPixelLocation",POINT),
              ("ptHimetricLocation",POINT),
              ("ptPixelLocationRaw",POINT),
              ("ptHimetricLocationRaw",POINT),
              ("dwTime",DWORD),
              ("historyCount",c_uint32),
              ("inputData",c_int32),
              ("dwKeyStates",DWORD),
              ("PerformanceCount",c_uint64),
              ("ButtonChangeType",c_int)
              ]


class POINTER_TOUCH_INFO(Structure):
    _fields_=[("pointerInfo",POINTER_INFO),
              ("touchFlags",c_int),
              ("touchMask",c_int),
              ("rcContact", RECT),
              ("rcContactRaw",RECT),
              ("orientation", c_uint32),
              ("pressure", c_uint32)]



#Initialize Pointer and Touch info

pointerInfo=POINTER_INFO(pointerType=PT_TOUCH,
                         pointerId=0,
                         ptPixelLocation=POINT(1280,720))

touchInfo=POINTER_TOUCH_INFO(pointerInfo=pointerInfo,
                             touchFlags=TOUCH_FLAG_NONE,
                             touchMask=TOUCH_MASK_ALL,
                             rcContact=RECT(pointerInfo.ptPixelLocation.x-5,
                                  pointerInfo.ptPixelLocation.y-5,
                                  pointerInfo.ptPixelLocation.x+5,
                                  pointerInfo.ptPixelLocation.y+5),
                             orientation=90,
                             pressure=32000)


def makeTouch(x,y,fingerRadius):
    touchInfo.pointerInfo.ptPixelLocation.x=x
    touchInfo.pointerInfo.ptPixelLocation.y=y

    touchInfo.rcContact.left=x-fingerRadius
    touchInfo.rcContact.right=x+fingerRadius
    touchInfo.rcContact.top=y-fingerRadius
    touchInfo.rcContact.bottom=y+fingerRadius

    #Initialize Touch Injection
    if (windll.user32.InitializeTouchInjection(1,1) != 0):
        print("Initialized Touch Injection")

    #Press Down
    touchInfo.pointerInfo.pointerFlags=(POINTER_FLAG_DOWN|
                                        POINTER_FLAG_INRANGE|
                                        POINTER_FLAG_INCONTACT)

    if (windll.user32.InjectTouchInput(1, byref(touchInfo))==0):
        print("Failed with Error: "+ FormatError())

    else:
        print("Touch Down Succeeded!")

    #Pull Upcc
    touchInfo.pointerInfo.pointerFlags=POINTER_FLAG_UP

    if (windll.user32.InjectTouchInput(1,byref(touchInfo))==0):
        print("Failed with Error: "+FormatError())

    else:
        print("Pull Up Succeeded!")

    return

def handler(signal_received, frame):
    global run_code
    # Handle any cleanup here
    if signal_received == SIGINT:
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        run_code = False

def Main(s):
    #controller = mouse.Controller()
     # Query DPI Awareness (Windows 10 and 8)
    windll.shcore.SetProcessDpiAwareness(2)
    awareness = c_int()
    errorCode = windll.shcore.GetProcessDpiAwareness(0, byref(awareness))
    print("DPI Awareness: ", awareness.value)

    while True:
         # reveive data from socket connection
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        event = tuple(map(int, data.split(',')))
        print("Raw data", data)
        print("Message from: " + str(addr))
        print("From connected client: " + str(event))
        touch = event[0]
        posX = int(width / MAX * event[2])
        posY = int(height / MAX * event[3])
        #controller.position = (posX, posY)
        if touch == 0:
            # on touchup (release)
            print(posX, posY, 5)
            makeTouch(posX, posY, 5)
            #controller.click(mouse.Button.left, 1)

        # TODO: add double click support
        # TODO: add finger press and move support for painting and marking


if __name__=='__main__':
    run_code = True
    host = os.environ.get("HOST_IP", '') #Server ip
    port = int(os.environ.get("HOST_PORT", 4000))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    
    program = Process(target=Main, args=(s,))
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)
    print('Running. Press CTRL-C to exit.')

    # Start Main
    program.start()
    print("Server start listening on {0} and port {1}".format(host, port))

    while run_code:
        # run forever
        pass
    
    # Clean up
    program.terminate()
    s.close()
