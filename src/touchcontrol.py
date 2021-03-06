#!/usr/bin/env python3

import os, time
from evdev import InputDevice, util, ecodes as e
from selectors import DefaultSelector, EVENT_READ
import serial

version = "1.0.0"

# function for sending the event to the serial adapter 
def send_event(num, touch, finger, x, y):
    real_x = round(10000 / 0x7FFF * x)
    real_y = round(10000 / 0x7FFF * y)
    width = 10000 / monitors
    xx = round(real_x / monitors + (width * num))

    string = "{},{},{},{}\n".format(touch, finger, xx, real_y)
    ser.write(string.encode())
    print(string)

# function for checking device status
def check_missing_devices():
    """ checks if paths of missing devices are available """
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


if __name__ == '__main__':

    print("Starting sc_tc.py version:", version)

    # Number of display monitors
    monitors = int(os.environ.get("MONITORS", 4))

    # Threshold and Deadzones
    threshold = 0.02
    deadzone_left = round(0x7FFF * threshold)
    deadzone_right = 0x7FFF - deadzone_left

    # Serial Adapter for sending touch events
    ser = serial.Serial('/dev/ttyUSB0', 115200)

    # Array of input devices.These pathes never changes for the same computer.
    input_devices = [
            '/dev/input/by-path/pci-0000:00:14.0-usb-0:1.3:1.3-event',
            '/dev/input/by-path/pci-0000:00:14.0-usb-0:2.3:1.3-event',
            '/dev/input/by-path/pci-0000:00:14.0-usb-0:3.3:1.3-event'
    ]

    # Array of missing devices
    missing_devices = []
    
    # File selector for reading values from input devices
    selector = DefaultSelector()
    state = {}

    # loop over input devices and try to register them for later reading. 
    # In case of an exeption the missing input will be saved in the missing input array 
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

        # Initialize state of device
        state[i] = {
            'slots': {}, 
            'current': 0
        }
    
    print(state)
    
    while True:
        # make sure there are no missing input devices
        if len(missing_devices) > 0:
            check_missing_devices()

        # retry to find missing imput device after 3 seconds
        if len(missing_devices) > 0:
            time.sleep(3)
            continue

        # collect values from input devices
        for key, mask in selector.select():
            device = key.fileobj
            # set device number
            num = key.data

            # read device values
            for event in device.read():

                code = None
                if event.type == e.EV_SYN:
                    code = e.SYN[event.code]
                elif event.type == e.EV_ABS:
                    code = e.ABS[event.code]

                if code == None:
                    continue

                print("num: {}, code: {}, value: {}".format(num, code, event.value))

                # set current slot in state
                c = state[num]['current']

                # event report and send
                if event.type == e.EV_SYN and event.code == e.SYN_REPORT:
                    for k, v in list(state[num]['slots'].items()):
                        if (v['x'] > 0 and v['y'] > 0):
                            send_event(num, v['touch'], k, v['x'], v['y'])
                        if v['touch'] == 0:
                            send_event(num, v['touch'], k, v['x'], v['y'])
                            del(state[num]['slots'][k])

                # event slot number
                if event.code == e.ABS_MT_SLOT:
                    # change to slot number
                    state[num]['current'] = event.value

                # event tracking. event.value > 0 means touch down.
                elif event.code == e.ABS_MT_TRACKING_ID:

                    # check if touch is down or up
                    if event.value > 0:
                        # touch is down
                        state[num]['slots'][c] = {'touch': 1, 'x': 0, 'y': 0}
                    else:
                        # touch is up
                        state[num]['slots'][c] = {'touch': 0, 'x': 0, 'y': 0}

                # event x-position
                elif event.code == e.ABS_MT_POSITION_X:
                    # make sure x-position is not in the deadzone eg. ghost touches
                    if event.value > deadzone_left and event.value < deadzone_right:
                        state[num]['slots'][c]['x'] = event.value
                    else:
                        print("Ghosttouch X:{}".format(event.value))

                elif event.code == e.ABS_MT_POSITION_Y:
                    state[num]['slots'][c]['y'] = event.value
