#!/usr/bin/env python3

import wx, wx.lib.newevent, time
from pynput import keyboard
from threading import *

KeyMemoEvent, EVT_KEYMEMO = wx.lib.newevent.NewEvent()

class KeyCtrl(Thread):

    # initialize
    keys = []
    wxWindow = None
    timeout = 2

    _timestamp = time.time()
    _memo = []
    _proc = None

    def __init__(self, wxWindow, keys=[], timeout=2):
        super(KeyCtrl, self).__init__()
        self.keys = keys
        self.wxWindow = wxWindow
        self.timeout = timeout

    def checkMemorizedKeys(self, str):
        print("store: {}".format(str))
        return str in self.keys

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
                    #print('Received event {}'.format(event))
                    #print('KeyMemo {}'.format(keymemo))

                    # if memo is not empty open url in chrome, reset memo and clear key memory
                    if found:
                        evt = KeyMemoEvent(memo=search)
                        wx.PostEvent(self.wxWindow, evt)
                        self._memo.clear()
                        found = -1

    
