#!/usr/bin/env python3

import os, socket, time
from dotenv import load_dotenv
load_dotenv()

# Socket
host = os.environ.get("HOST_IP")
port = int(os.environ.get("HOST_PORT"))
server = (host, port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(server)
print("Connected to host: {0} on port {1}".format(host, port))
print("My IP addresse is {}".format(s.getsockname()[0]))

def send_event(num, touch, finger, x, y):
    real_x = round(10000 / 0x7FFF * x)
    real_y = round(10000 / 0x7FFF * y)
    width_per_mon = 10000 / monitors
    #width_per_mon = 10000 / len(input_devices)
    xx = round(real_x / monitors + (width_per_mon * num))

    string = "{},{},{},{}\n".format(touch, finger, xx, real_y)
    #ser.write(string.encode())
    s.sendto(string.encode('utf-8'), server)
    print(string)

if __name__ == '__main__':

    monitors = 1

    send_event(0, 1, 0, 6982, 5642)
    time.sleep(0.1)
    send_event(0, 0, 0, 0x7FFF / 2, 0x7FFF / 2)
    # time.sleep(0.1)
    # send_event(0, 1, 0, 6982, 5642)
    # time.sleep(0.1)
    # send_event(0, 0, 0, 6982, 5642)
    # time.sleep(3)
    # send_event(0, 1, 0, 6982, 5642)
    # time.sleep(0.1)
    # send_event(0, 0, 0, 6982, 5642)
    # time.sleep(0.1)
    # send_event(0, 1, 0, 6982, 5642)
    for i in range(1, 10):
        send_event(0, 0, 0, (0x7FFF / 2), 5000)
        time.sleep(6.61)
    # send_event(0, 0, 0, 6982, 15642)
    # time.sleep(3)
    # send_event(0, 0, 0, 6982, 5642)
    # time.sleep(2)
    # send_event(0, 1, 0, 6982, 5642)
    # time.sleep(0.1)
    # send_event(0, 0, 0, 6982, 5642)
