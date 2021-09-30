#!/usr/bin/env python3

import ctypes
import win32api
from pprint import pprint
import tkinter
import wx


PROCESS_PER_MONITOR_DPI_AWARE = 2
MDT_EFFECTIVE_DPI = 0
ID_MENU_EXIT = wx.NewIdRef()
ID_MENU_PREF = wx.NewIdRef()

ID_PANEL_PREF = wx.NewIdRef()

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

class MyApp(wx.App):
    def OnInit(self):
        return super().OnInit()

class PreferencesDialog(wx.Dialog):

    ID_LIST = wx.NewIdRef()

    listItems = [
        ('name1', 'key1', 'http://www.barasi.de'), 
        ('name2', 'key2', 'http://www.nakedtoast.de'), 
        ('name3', 'key3', 'http://www.nelsen-consulting.de')
    ]

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.InitUI()
        self.SetSize((250, 200))
        self.SetTitle("Change Preferences")

    def InitUI(self):

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        lc = wx.ListCtrl(pnl, wx.ID_ANY, style=wx.LC_REPORT)
        lc.InsertColumn(0, 'name')
        lc.InsertColumn(0, 'key')
        lc.InsertColumn(1, 'value', width=wx.LIST_AUTOSIZE_USEHEADER)
        for i in range(len(self.listItems)):
            print(i, self.listItems[i][0], self.listItems[i][1])
            lc.InsertItem(i, self.listItems[i][0])
            lc.SetItem(i, 1, self.listItems[i][1])
            lc.SetItem(i, 2, self.listItems[i][2])

        sb = wx.StaticBox(pnl, label='Registered Keys')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
        sbs.Add(lc, flag=wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        addButton = wx.Button(self, label='+')
        deleteButton = wx.Button(self, label='-')
        hbox.Add(addButton)
        hbox.Add(deleteButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        pnl.SetSizer(sbs)
        self.SetSizer(vbox)

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MyFrame, self).__init__(*args, **kw)
        panel = wx.Panel(self, wx.ID_ANY)
        basicLabel = wx.StaticText(panel, label="Basic Control:")
        self.basicText = wx.TextCtrl(panel, size=(175, -1))
        pwdLabel = wx.StaticText(panel, label="Password:")
        pwdText = wx.TextCtrl(panel, size=(175, -1), style=wx.TE_PASSWORD)
        btn = wx.Button(panel, label='Save')
        btn.Bind(wx.EVT_BUTTON, self.onSave)

        sizer = wx.BoxSizer(wx.VERTICAL)

        fsizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        fsizer.Add(basicLabel, 1, wx.ALIGN_CENTRE_VERTICAL)
        fsizer.Add(self.basicText, 1)
        fsizer.Add(pwdLabel, 1, wx.ALIGN_CENTRE_VERTICAL)
        fsizer.Add(pwdText, 1)
        
        sizer.Add(fsizer, flag=wx.EXPAND|wx.ALL, border=10)
        fsizer.AddSpacer(0)
        fsizer.Add(btn, 0, wx.ALIGN_RIGHT)

        panel.SetSizer(sizer)
        self.Bind(wx.EVT_DPI_CHANGED, self.OnDPIChanged)
        self.Bind(wx.EVT_DISPLAY_CHANGED, self.OnDisplayChanged)

        self.InitUI()

    def InitUI(self):
        tb = self.CreateToolBar()
        tb.AddTool(toolId=wx.ID_ANY, label='', bitmap=wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW))
        tb.Realize()
        tb.Bind(wx.EVT_TOOL, self.OnChangeList)

        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        pmi = wx.MenuItem(fileMenu, ID_MENU_PREF, '&Preferences\tCtrl+P')
        qmi = wx.MenuItem(fileMenu, ID_MENU_EXIT, '&Quit\tCtrl+Q')
        qmi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_QUIT))
        pmi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE))
        fileMenu.Append(pmi)
        fileMenu.Append(qmi)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnMenuClick, pmi)
        self.Bind(wx.EVT_MENU, self.OnMenuClick, qmi)

        # panel
        panel = wx.Panel(self, ID_PANEL_PREF)

    def OnChangeList(self, e):
        prefDialog = PreferencesDialog(None, title='Preferences', style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        prefDialog.ShowModal()
        prefDialog.Destroy()

    def OnMenuClick(self, e):
        eid = e.GetId()
        print("clicked", eid)
        if eid == ID_MENU_PREF:
            print("pref click")
        elif eid == ID_MENU_EXIT:
            print("quit click")
            self.Close()
        
    def OnQuit(self, e):
        self.Close()

    def OnDPIChanged(self, event):
        print(ctypes.windll.user32.GetDpiForSystem())
    
    def OnDisplayChanged(self, event):
        print("width: ", ctypes.windll.user32.GetSystemMetrics(78))
        print("height: ", ctypes.windll.user32.GetSystemMetrics(79))
        print_dpi()

    def onSave(self, event):
        print(self.basicText.Value)

def main():
    app = MyApp()
    frm = MyFrame(None, title='Hello World 2')
    frm.Show()
    app.MainLoop()

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

    # # Set DPI Awareness  (Windows 10 and 8)
    # # the argument is the awareness level, which can be 0, 1 or 2:
    # # for 1-to-1 pixel control I seem to need it to be non-zero (I'm using level 2)
    errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
    if errorCode is 0:
        awareness = ctypes.c_int()
        awareness = ctypes.c_int()
        ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
        print("successfully changed dpi awareness to {}".format(awareness.value))
    else:
        print("failed to change dpi awareness")

    # print('---')
    
    # from win32con import LOGPIXELSX
    # success = ctypes.windll.user32.SetProcessDPIAware()
    # hDC = ctypes.windll.user32.GetDC(None)
    # print(ctypes.windll.gdi32.GetDeviceCaps( hDC, LOGPIXELSX))

    # print('---')
    # print(ctypes.windll.user32.GetDpiForSystem())

    main()

    