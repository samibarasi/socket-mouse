#!/usr/bin/env python3
import socket, os, time
from dotenv import load_dotenv
from pynput import mouse
from signal import signal, SIGINT
from multiprocessing import Process
from pprint import pprint

load_dotenv()

from ctypes import *
from ctypes.wintypes import *
from threading import *

#Constants

# For touch screen values
MAX = 10000

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

screenWidth = windll.user32.GetSystemMetrics(78)
screenHeight = windll.user32.GetSystemMetrics(79)

def makeTouch(x,y,fingerRadius):
    print("maketouch:", x, y, fingerRadius)
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

    print("\n")

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
        print("Message from: " + str(addr))
        print("From connected client: " + str(event))
        print("Raw data", data)
        touch = event[0]
        posX = int(screenWidth / MAX * event[2])
        posY = int(screenHeight / MAX * event[3])
        #controller.position = (posX, posY)
        if touch == 0:
            # on touchup (release)
            makeTouch(posX, posY, 5)
            #controller.click(mouse.Button.left, 1)

        # TODO: add double click support
        # TODO: add finger press and move support for painting and marking
        # TODO: add multi touch support


class TouchCtrl(Thread):

    def __init__(self, wxWindow):
        super(TouchCtrl, self).__init__()
        self.wxWindow = wxWindow
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def update(self, dim):
        global screenWidth, screenHeight
        print(dim)
        screenWidth = dim[0]['screenWidth']
        screenHeight = dim[0]['screenHeight']
        print("update touchcontrol metrics to {} x {}".format(screenWidth, screenHeight))

    def run(self):
        host = os.environ.get("HOST_IP", '') #Server ip
        port = int(os.environ.get("HOST_PORT", 4000))

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))

        program = Process(target=Main, args=(s,))

        # Start Main
        program.start()
        print("Server start listening on {0} and port {1}".format(host, port))

        while not self._stop_event.is_set():
            # run forever
            time.sleep(1)
            # posX = int(screenWidth / MAX * 5000)
            # posY = int(screenHeight / MAX * 2500)
            # makeTouch(posX, posY, 5)
            pass

        # Clean up
        program.terminate()
        s.close()
        print("touch control has closed socket and was terminated.")