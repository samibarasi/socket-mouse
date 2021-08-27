import keyboard
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
    
    print("open {}".format(url))

    # Open URL in Chrome
    proc = Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe", "-kiosk", url])

def key_press(key):
    global timestamp

    # Append pressed key to key memory
    try:
        keymemo.append(key.name)
    except AttributeError:
        pass

    # Build string from key memory and check if it's a known one.
    memo = checkMemorizedKeys("".join(str(i) for i in keymemo))

    timestamp = time.time()
    #print('Received key {}'.format(key.name))
    #print('KeyMemo {}'.format(keymemo))

    # if memo is not empty open url in chrome, reset memo and clear key memory
    if memo:
        openURL(memo)
        keymemo.clear()
        memo = ""

if __name__ == "__main__":
    # initialize
    timeout = 2
    timestamp = time.time()
    keymemo = []

    # Open Chrome with default Page e.g. _blank
    proc = Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe", "-kiosk", "about:blank"])

    # Start listening to key event 
    keyboard.on_press(key_press)

    while True:
        # if time is up clear key memory
        if timestamp + timeout < time.time():
            keymemo.clear()
        time.sleep(1)