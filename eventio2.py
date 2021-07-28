import socket, os, json
from evdev import InputDevice
from selectors import DefaultSelector, EVENT_READ
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

selector = DefaultSelector()
#dev1 = InputDevice('/dev/input/by-path/pci-0000:00:14.0-usb-0:1.3:1.3-event')
dev2 = InputDevice('/dev/input/by-path/pci-0000:00:14.0-usb-0:2.3:1.3-event')
#dev3 = InputDevice('/dev/input/by-path/pci-0000:00:14.0-usb-0:3.3:1.3-event')
#dev4 = InputDevice('/dev/input/by-path/pci-0000:00:14.0-usb-0:4.3:1.3-event')

# This works because InputDevice has a `fileno()` method.
selector.register(dev1, EVENT_READ, 0)
#selector.register(dev2, EVENT_READ, 1)
#selector.register(dev3, EVENT_READ, 2)
#selector.register(dev4, EVENT_READ, 4)

while True:
    for key, mask in selector.select():
        device = key.fileobj
        num = key.data
        for event in device.read():
            #print(str(num) + ":", "code: " + str(event.code), "type: " + str(event.type), "value: " + str(event.value))
            print("num: {:d}, code: {:d}, type: {:d}, value: {:d}".format(num, event.code, event.type, event.value))
            if event.code == 0 and event.type == 3:
                posX = event.value
            if event.code == 1 and event.type == 3:
                posY = event.value
            if event.code == 1 or event.code == 0 or event.code == 330:
                message = {
                    "num": num,
                    "code": event.code,
                    "type": event.type,
                    "value": event.value
                }
                jsonStr = json.dumps(message)
                print(jsonStr)
                #message = "{:d},{:d},{:d}".format(event.type, posX, posY)

                s.sendto(jsonStr.encode('utf-8'), server)
