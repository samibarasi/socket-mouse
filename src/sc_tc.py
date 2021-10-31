#!/usr/bin/env python3

import os, socket, time
from dotenv import load_dotenv
load_dotenv()
from evdev import InputDevice, util, ecodes as e
from selectors import DefaultSelector, EVENT_READ

# Socket
host = os.environ.get("HOST_IP")
port = int(os.environ.get("HOST_PORT"))
server = (host, port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(server)
print("Connected to host: {0} on port {1}".format(host, port))
print("My IP addresse is {}".format(s.getsockname()[0]))

# function for sending the event to the server 
def send_event(num, touch, finger, x, y):
    real_x = round(10000 / 0x7FFF * x)
    real_y = round(10000 / 0x7FFF * y)
    width = 10000 / monitors
    xx = round(real_x / monitors + (width * num))

    string = "{},{},{},{}\n".format(touch, finger, xx, real_y)
    #ser.write(string.encode())
    s.sendto(string.encode('utf-8'), server)
    print(string)

# function for checking device status
def check_missing_devices():
    global missing_devices
    i = 0
    while i < len(missing_devices):
        path = input_devices[missing_devices[i]]
        print(path)
        if os.path.exists(path):
            # Found missing device. register and remove missing device index from missing device list.
            print("found missing device {}: {}".format(missing_devices[i], path))
            selector.register(
                InputDevice(input_devices[missing_devices.pop(i)]),
                EVENT_READ,
                i
            )
        else:
            # Still missing.
            i += 1

# main program
if __name__ == '__main__':

    monitors = 4
    threshold = 0.02

    deadzone_left = round(0x7FFF * threshold)
    deadzone_right = 0x7FFF - deadzone_left

    #ser = serial.Serial('/dev/ttyUSB0', 115200)

    # array of input devices resources
    input_devices = [
            '/dev/input/by-path/pci-0000:00:14.0-usb-0:1.3:1.3-event',
            '/dev/input/by-path/pci-0000:00:14.0-usb-0:2.3:1.3-event',
            '/dev/input/by-path/pci-0000:00:14.0-usb-0:3.3:1.3-event'
    ]

    missing_devices = []
    
    selector = DefaultSelector()
    state = {}

    for i in range(len(input_devices)):
        try:
            selector.register(
                InputDevice(input_devices[i]),
                EVENT_READ,
                i
            )
        except:
            missing_devices.append(i)
            continue
        state[i] = {'slots': {}, 'current': 0}
    
    print(state)

    while True:
        if len(missing_devices) > 0:
            check_missing_devices()

        if len(missing_devices) > 0:
            time.sleep(3)
            continue

        for key, mask in selector.select():
            device = key.fileobj
            num = key.data
            
            for event in device.read():

                code = None
                if event.type == e.EV_SYN:
                    code = e.SYN[event.code]
                elif event.type == e.EV_ABS:
                    code = e.ABS[event.code]

                if code == None:
                    continue

                print("num: {}, code: {}, value: {}".format(num, code, event.value))

                c = state[num]['current']

                if event.type == e.EV_SYN and event.code == e.SYN_REPORT:
                    for k, v in list(state[num]['slots'].items()):
                        #if (v['x'] > 0 and v['y'] > 0):
                        if v['touch'] == 1:
                            send_event(num, v['touch'], k, v['x'], v['y'])

                        if v['touch'] == 0:
                            send_event(num, v['touch'], k, v['x'], v['y'])
                            del(state[num]['slots'][k])

                if event.code == e.ABS_MT_SLOT:
                    state[num]['current'] = event.value

                elif event.code == e.ABS_MT_TRACKING_ID:
                    if event.value > 0:
                        state[num]['slots'][c] = {'touch': 1, 'x': 0, 'y': 0}
                    else:
                        #state[num]['slots'][c] = {'touch': 0, 'x': 0, 'y': 0}
                        state[num]['slots'][c]['touch'] = 0

                elif event.code == e.ABS_MT_POSITION_X:
                    if event.value > deadzone_left and event.value < deadzone_right:
                        state[num]['slots'][c]['x'] = event.value
                    else:
                        print("Ghosttouch X:{}".format(event.value))

                elif event.code == e.ABS_MT_POSITION_Y:
                    state[num]['slots'][c]['y'] = event.value

