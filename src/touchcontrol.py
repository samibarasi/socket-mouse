#!/usr/bin/env python3

from evdev import InputDevice, util, ecodes as e
from selectors import DefaultSelector, EVENT_READ
import serial

def send_event(touch, finger, x, y):
    real_x = round(10000 / 0x7FFF * x)
    real_y = round(10000 / 0x7FFF * y)
    string = "{},{},{},{}\n".format(touch, finger, real_x, real_y)
    ser.write(string.encode())
    print(string)


if __name__ == '__main__':

    mixed_events = False

    ser = serial.Serial('/dev/ttyUSB0', 115200)


    input_devices = [
        '/dev/input/by-path/pci-0000:00:14.0-usb-0:3.3:1.0-event'
    ]

    selector = DefaultSelector()
    state = {}


    for i in range(len(input_devices)):
        selector.register(
            InputDevice(input_devices[i]),
            EVENT_READ,
            i
        )
        state[i] = {'slots': {}, 'current': 0}

    while True:
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
                        send_event(v['touch'], k, v['x'], v['y'])
                        if v['touch'] == 0:
                            del(state[num]['slots'][k])
                
                if event.code == e.ABS_MT_SLOT:
                    state[num]['current'] = event.value

                elif event.code == e.ABS_MT_TRACKING_ID:
                    if event.value > 0:
                        state[num]['slots'][c] = {'touch': 1, 'x': 0, 'y': 0}
                    else:
                        state[num]['slots'][c] = {'touch': 0, 'x': 0, 'y': 0}

                elif event.code == e.ABS_MT_POSITION_X:
                    state[num]['slots'][c]['x'] = event.value

                elif event.code == e.ABS_MT_POSITION_Y:
                    state[num]['slots'][c]['y'] = event.value
