import csv, time, os
from pynput import keyboard
from subprocess import Popen
from signal import signal, SIGINT
from threading import *

class KeyCtrl(Thread):

    # initialize
    keys = []
    callback = None
    timeout = 2

    _timestamp = time.time()
    _memo = []

    def __init__(self, callback=None, keys=[], timeout=2):
        super(KeyCtrl, self).__init__()
        self.keys = keys
        self.callback = callback
        self.timeout = timeout
        self.lock = RLock()
        self.daemon = True

    def checkMemorizedKeys(self, str):
        print("store: {}".format(str))
        with self.lock:
            return str in self.keys

    def SetKeys(self, keys):
        with self.lock:
            self.keys = keys

    def run(self):
        found = False
        # The event listener will be running in this block
        with keyboard.Events() as events:
            for event in events:
                if self._timestamp + self.timeout < time.time():
                    self._memo.clear()
                if isinstance(event, keyboard.Events.Press):
                    # Append pressed key to key memory
                    try:
                        self._memo.append(event.key.char)
                    except AttributeError:
                        pass

                    # Build string from key memory and check if it's a known one.
                    search = "".join(str(i) for i in self._memo)
                    found = self.checkMemorizedKeys(search)

                    self._timestamp = time.time()

                    # if memo is not empty call callback function, reset memo and clear key memory
                    if found:
                        if self.callback:
                            self.callback(memo=search)
                        self._memo.clear()
                        found = -1

def handler(signal_received, frame):
    global run_code
    # Handle any cleanup here
    if signal_received == SIGINT:
        print('SIGINT or CTRL-C detected. Exiting gracefully')
        run_code = False

def GetUrlByKey(key):
    for x in bookmarks:
        if (x[1] == key):
            return x[2]

def OnKeyMemo(memo):
    print("key memo: {}".format(memo))
    url = GetUrlByKey(memo)
    if url:
        OpenURL(url)
    else:
        raise ValueError('url for key not found!')

def OpenURL(url):
    global proc_chrome

    # Check if Chrome is still running and if yes, kill it :-D
    if proc_chrome and proc_chrome.poll() is None:
        proc_chrome.terminate()

    # Open URL in Chrome
    proc_chrome = Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe", "-kiosk", url])

def main():
    global bookmarks, keyctrl, filename

    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)

    # Read bookmarks from file
    with open(filename, newline='') as csvfile:
        bookmarkreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in bookmarkreader:
            bookmarks.append((row[0], row[1], row[2]))

    # Key control
    listOfKeys = [x[1] for x in bookmarks]
    # Create Key Control Thread and provide a callback function to the keyctrl class
    keyctrl = KeyCtrl(OnKeyMemo, listOfKeys)
    keyctrl.start()

if __name__ == "__main__":
    _cached_stamp = 0
    filename = 'bookmarks.csv'
    bookmarks = []
    keyctrl = None
    proc_chrome = None
    run_code = True
    main()

    while run_code:
        time.sleep(1)
        stamp = os.stat(filename).st_mtime
        if stamp != _cached_stamp:
            _cached_stamp = stamp
            bookmarks = []
            # Read bookmarks from file
            with open(filename, newline='') as csvfile:
                bookmarkreader = csv.reader(csvfile, delimiter=';', quotechar='"')
                for row in bookmarkreader:
                    bookmarks.append((row[0], row[1], row[2]))
            # Update list of keyctrl keys
            keys = [x[1] for x in bookmarks]
            keyctrl.SetKeys(keys)
