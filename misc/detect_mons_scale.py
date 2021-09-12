#!/usr/bin/env python3

import ctypes
import win32api
from pprint import pprint
import tkinter
import wx


PROCESS_PER_MONITOR_DPI_AWARE = 2
MDT_EFFECTIVE_DPI = 0

def print_dpi():
    shcore = ctypes.windll.shcore
    monitors = win32api.EnumDisplayMonitors()
    # hresult = shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    # print(hresult)
    # assert hresult == 0
    dpiX = ctypes.c_uint()
    dpiY = ctypes.c_uint()
    for i, monitor in enumerate(monitors):
        shcore.GetDpiForMonitor(
            monitor[0].handle,
            MDT_EFFECTIVE_DPI,
            ctypes.byref(dpiX),
            ctypes.byref(dpiY)
        )
        print(
            f"Monitor {i} (hmonitor: {monitor[0]}) = dpiX: {dpiX.value}, dpiY: {dpiY.value}"
        )

def OnFrameExit(event):
    # Do something useful.
    pass


if __name__ == "__main__":
    print_dpi()

    screen_x = ctypes.windll.user32.GetSystemMetrics(0)
    screen_y = ctypes.windll.user32.GetSystemMetrics(1)

    print(screen_x, screen_y)

    screen_x = ctypes.windll.user32.GetSystemMetrics(78)
    screen_y = ctypes.windll.user32.GetSystemMetrics(79)

    print(screen_x, screen_y)

    # root = tkinter.Tk()
    # dpi = root.winfo_fpixels('1i')

    # print(round(dpi))

    # print('---')

    # # Query DPI Awareness (Windows 10 and 8)
    awareness = ctypes.c_int()
    errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
    print(awareness.value)

    # # Set DPI Awareness  (Windows 10 and 8)
    errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
    print(errorCode)
    # # the argument is the awareness level, which can be 0, 1 or 2:
    # # for 1-to-1 pixel control I seem to need it to be non-zero (I'm using level 2)
    
    # print('---')
    
    # from win32con import LOGPIXELSX
    # success = ctypes.windll.user32.SetProcessDPIAware()
    # hDC = ctypes.windll.user32.GetDC(None)
    # print(ctypes.windll.gdi32.GetDeviceCaps( hDC, LOGPIXELSX))

    # print('---')
    # print(ctypes.windll.user32.GetDpiForSystem())

    class MyApp(wx.App):
        def OnInit(self):
            return super().OnInit()

    class MyFrame(wx.Frame):
        def __init__(self, *args, **kw):
            # ensure the parent's __init__ is called
            super(MyFrame, self).__init__(*args, **kw)
            self.Bind(wx.EVT_DPI_CHANGED, self.OnDPIChanged)
            self.Bind(wx.EVT_DISPLAY_CHANGED, self.OnDisplayChanged)

        def OnDPIChanged(self, event):
            print(ctypes.windll.user32.GetDpiForSystem())
        
        def OnDisplayChanged(self, event):
            print("width: ", ctypes.windll.user32.GetSystemMetrics(78))
            print("height: ", ctypes.windll.user32.GetSystemMetrics(79))
            print("dpi:", ctypes.windll.user32.GetDpiForSystem())
            print_dpi()

    app = MyApp()
    frm = MyFrame(None, title='Hello World 2')
    frm.Show()
    app.MainLoop()