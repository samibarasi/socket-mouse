from pynput import keyboard
import time
from subprocess import Popen

def checkMemorizedKeys(str):
    #print("store: {}".format(str))
    switcher = {
        "abc": "http://barasi.gmbh",
        "cde": "http://nelsen-consulting.de"
    }
    return switcher.get(str, "")

def openURL(url):
    global proc

    # Check if Chrome is still running and if yes, kill it :-D
    if proc.poll() is None:
        proc.terminate()

    # Open URL in Chrome
    proc = Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe", "-kiosk", url])

if __name__ == "__main__":
    # initialize
    timeout = 2
    timestamp = time.time()
    keymemo = []

    # Open Chrome with default Page e.g. _blank
    proc = Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe", "-kiosk", "about:blank"])

    # The event listener will be running in this block
    with keyboard.Events() as events:
        for event in events:
            if timestamp + timeout < time.time():
                keymemo.clear()
            if isinstance(event, keyboard.Events.Press):
                # Append pressed key to key memory
                try:
                    keymemo.append(event.key.char)
                except AttributeError:
                    pass
                
                # Build string from key memory and check if it's a known one.
                memo = checkMemorizedKeys("".join(str(i) for i in keymemo))

                timestamp = time.time()
                #print('Received event {}'.format(event))
                #print('KeyMemo {}'.format(keymemo))

                # if memo is not empty open url in chrome, reset memo and clear key memory
                if memo:
                    openURL(memo)
                    keymemo.clear()
                    memo = ""
