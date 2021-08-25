from pynput import keyboard
import time

timestamp = time.time()
keymemo = []

print("Timestamp: {}".format(timestamp))
print("Timestamp: {}".format(int(timestamp)))

def checkMemo(str):
    print(str)
    switcher = {
        "abc": "ABC",
        "cde": "CDE"
    }
    return switcher.get(str, "")

# The event listener will be running in this block
with keyboard.Events() as events:
    for event in events:
        if timestamp + 5 < time.time():
            keymemo.clear()
        if isinstance(event, keyboard.Events.Press):
            if event.key == keyboard.Key.esc:
                break
            else:
                try:
                    keymemo.append(event.key.char)
                except AttributeError:
                    pass
                print(checkMemo("".join(str(i) for i in keymemo)))
                timestamp = time.time()
                print('Received event {}'.format(event))
                print('KeyMemo {}'.format(keymemo))

# Open chrome in kiosk mode: "C:\Program Files\Google\Chrome\Application\chrome.exe" -kiosk http://praxistipps.chip.de/ --overscroll-history-navigation=0
# or "C:\Program Files\Google\Chrome\Application\chrome.exe" -kiosk http://praxistipps.chip.de/ --overscroll-history-navigation=0