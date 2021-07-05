from evdev import InputDevice
from selectors import DefaultSelector, EVENT_READ

selector = selectors.DefaultSelector()

mouse = evdev.InputDevice('/dev/input/event1')
keybd = evdev.InputDevice('/dev/input/event2')

# This works because InputDevice has a `fileno()` method.
selector.register(mouse, selectors.EVENT_READ)
selector.register(keybd, selectors.EVENT_READ)

while True:
    for key, mask in selector.select():
        device = key.fileobj
        for event in device.read():
            print(event)