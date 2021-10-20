#!/usr/bin/env python3

from sys import flags
import wx
from wx.lib.newevent import NewEvent
from wx.core import EVT_BUTTON, EVT_LISTBOX


listItems = [
    ('name1', 'key1', 'http://www.barasi.de'), 
    ('name2', 'key2', 'http://www.nakedtoast.de'), 
    ('name3', 'key3', 'http://www.nelsen-consulting.de')
]

BookmarkNewEvent, EVT_BOOKMARK_NEW = NewEvent()


class PreferencesDialog(wx.Dialog):

    listItems = [
        ('name1', 'key1', 'http://www.barasi.de'), 
        ('name2', 'key2', 'http://www.nakedtoast.de'), 
        ('name3', 'key3', 'http://www.nelsen-consulting.de')
    ]

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.InitUI()
        self.SetSize((250, 200))
        #self.SetTitle("Change Preferences")

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

class MyApp(wx.App):
    def OnInit(self):
        return super().OnInit()

class MyPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(MyPanel, self).__init__(*args, **kw)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # panels array for easy access
        self.panels = [
            Panel1(self, MyFrame.ID_PANEL_REPORT),
            Panel2(self, MyFrame.ID_PANEL_PREF)
        ]

        for panel in self.panels:
            sizer.Add(panel, 1, wx.EXPAND)
            panel.Hide()

        self.SetSizer(sizer)
    
class Panel1(wx.Panel):
    def __init__(self, *args, **kw):
        super(Panel1, self).__init__(*args, **kw)
        self.SetBackgroundColour(wx.GREEN)
        self.title = wx.StaticText(self, label="Information:")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.title, flag=wx.EXPAND|wx.ALL, border=10)
       
        resolutionLabel = wx.StaticText(self, label="Resolution:")
        resolutionValue = wx.StaticText(self, MyFrame.ID_RESOLUTION, label="N/A")
        dpiLabel = wx.StaticText(self, label="DPI:")
        dpiValue = wx.StaticText(self, MyFrame.ID_DPI, label="N/A")

        fgs = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        fgs.Add(resolutionLabel, 1, wx.ALIGN_RIGHT)
        fgs.Add(resolutionValue, 1)
        fgs.Add(dpiLabel, 1, wx.ALIGN_RIGHT)
        fgs.Add(dpiValue, 1)

        sizer.Add(fgs, flag=wx.EXPAND|wx.ALL, border=10)

        self.SetSizer(sizer)

class Panel2(wx.Panel):

    dirty = False
    
    def __init__(self, *args, **kw):
        super(Panel2, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(self, label='Bookmarks')
        keyList = KeyList(sb, wx.ID_ANY)
        self.keyForm = KeyForm(sb, wx.ID_ANY)
        
        # lc = wx.ListCtrl(sb, wx.ID_ANY, style=wx.LC_REPORT)
        # lc.InsertColumn(0, 'name', wx.LIST_AUTOSIZE_USEHEADER)
        # lc.InsertColumn(1, 'key', wx.LIST_AUTOSIZE_USEHEADER)
        # for i in range(len(self.listItems)):
        #     print(i, self.listItems[i][0], self.listItems[i][1])
        #     lc.InsertItem(i, self.listItems[i][0])
        #     lc.SetItem(i, 1, self.listItems[i][1])

        keyList.Bind(EVT_BOOKMARK_NEW, self.OnBookmarkNew)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(keyList, flag=wx.EXPAND)
        hbox.Add(self.keyForm, 1, flag=wx.EXPAND|wx.LEFT, border=10)

        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
        sbs.Add(hbox, flag=wx.EXPAND)

        vbox.Add(sbs, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)

        self.SetSizer(vbox)

    def OnBookmarkNew(self, event):
        self.dirty = True
        print("New Bookmark event occurred with idx: {}".format(event.idx))
        print("len: {}".format(len(listItems)))
        self.keyForm.SetData(listItems[event.idx])

class KeyList(wx.Panel):

    ID_BTN_ADD = wx.NewIdRef()
    ID_BTN_DEL = wx.NewIdRef()

    def __init__(self, *args, **kw):
        super(KeyList, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        listOfNames = [x[0] for x in listItems]

        #self.SetBackgroundColour(wx.Colour("RED"))
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.lb = wx.ListBox(self, wx.ID_ANY, choices=listOfNames)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        addButton = wx.BitmapButton(self, self.ID_BTN_ADD, wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK))
        deleteButton = wx.BitmapButton(self, self.ID_BTN_DEL, wx.ArtProvider.GetBitmap(wx.ART_DEL_BOOKMARK))

        addButton.Bind(EVT_BUTTON, self.OnButtonClicked, addButton)
        self.lb.Bind(EVT_LISTBOX, self.OnListBoxSelected)
        #deleteButton = wx.Button(self, label='-', size=(20, 20))
        hbox.Add(addButton)
        hbox.AddStretchSpacer()
        hbox.Add(deleteButton)

        vbox.Add(self.lb, 1, flag=wx.EXPAND)
        vbox.Add(hbox, flag=wx.TOP|wx.EXPAND, border=5)
        self.SetSizer(vbox)

    def SetNames(self, names):
        self.lb.Clear()
        self.lb.InsertItems(names, 0)

    def OnButtonClicked(self, event):
        eid = event.GetId()
        print("button clicked: {}".format(eid))
        if eid == self.ID_BTN_ADD:
            self.NewBookmark()
        elif eid == self.ID_BTN_DEL:
            self.DelBookmark()

    def NewBookmark(self):
        listItems.append(('newItem', '', ''))
        new_idx = self.lb.GetCount()
        self.lb.InsertItems(['newItem'], new_idx)
        self.lb.SetSelection(new_idx)
        evt = BookmarkNewEvent(idx=new_idx)
        wx.PostEvent(self, evt)
        print(listItems)

    def OnListBoxSelected(self, event):
        print(self.lb.GetSelection())
        pass

    def DelBookmark(self):
        pass

class KeyForm(wx.Panel):
    def __init__(self, *args, **kw):
        super(KeyForm, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        #self.SetBackgroundColour(wx.Colour("GREEN"))
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        nameLabel = wx.StaticText(self, label="Name:")
        self.nameInput = wx.TextCtrl(self, wx.ID_ANY)
        keyLabel = wx.StaticText(self, label="Key:")
        self.keyInput = wx.TextCtrl(self, wx.ID_ANY)
        valueLabel = wx.StaticText(self, label="Value:")
        self.valueInput = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_CHARWRAP)
        saveBtn = wx.Button(self, wx.ID_ANY, label="Save")
        resetBtn = wx.Button(self, wx.ID_ANY, label="Reset")
        hbox.Add(resetBtn)
        hbox.Add(saveBtn)
        vbox.Add(nameLabel)
        vbox.Add(self.nameInput)
        vbox.Add(keyLabel, flag=wx.TOP, border=10)
        vbox.Add(self.keyInput)
        vbox.Add(valueLabel, flag=wx.TOP, border=10)
        vbox.Add(self.valueInput, 1, flag=wx.EXPAND)
        vbox.Add(hbox, 1, flag=wx.TOP|wx.ALIGN_RIGHT, border=10)
        self.SetSizer(vbox)

    def SetData(self, data):
        self.nameInput.SetValue(data[0])
        self.keyInput.SetValue(data[1])
        self.valueInput.SetValue(data[2])

class MyFrame(wx.Frame):
    ID_TOOL_REPORT = wx.NewIdRef()
    ID_TOOL_PREF = wx.NewIdRef()
    ID_PANEL_REPORT = wx.NewIdRef()
    ID_PANEL_PREF = wx.NewIdRef()
    ID_MENU_EXIT = wx.NewIdRef()
    ID_MENU_PREF = wx.NewIdRef()
    ID_RESOLUTION = wx.NewIdRef()
    ID_DPI = wx.NewIdRef()

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MyFrame, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        # Toolbar
        tb = self.CreateToolBar()
        tb.AddTool(toolId=self.ID_TOOL_REPORT, label='', bitmap=wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW))
        tb.AddTool(toolId=self.ID_TOOL_PREF, label='', bitmap=wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW))
        tb.Realize()
        tb.Bind(wx.EVT_TOOL, self.OnToolBarClicked)

        # Menu
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        pmi = wx.MenuItem(fileMenu, self.ID_MENU_PREF, '&Preferences\tCtrl+P')
        qmi = wx.MenuItem(fileMenu, self.ID_MENU_EXIT, '&Quit\tCtrl+Q')
        qmi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_QUIT))
        pmi.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE))
        fileMenu.Append(pmi)
        fileMenu.Append(qmi)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnMenuClick, pmi)
        self.Bind(wx.EVT_MENU, self.OnMenuClick, qmi)

        # Main Panel
        # panel = wx.Panel(self, self.ID_PANEL_REPORT)
        # resolutionLabel = wx.StaticText(panel, label="Resolution:")
        # resolutionValue = wx.StaticText(panel, self.ID_RESOLUTION, label="N/A")
        # dpiLabel = wx.StaticText(panel, label="DPI:")
        # dpiValue = wx.StaticText(panel, self.ID_DPI, label="N/A")

        # sizer = wx.BoxSizer(wx.VERTICAL)

        # fsizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        # fsizer.Add(resolutionLabel, 1, wx.ALIGN_RIGHT)
        # fsizer.Add(resolutionValue, 1)
        # fsizer.Add(dpiLabel, 1, wx.ALIGN_RIGHT)
        # fsizer.Add(dpiValue, 1)

        # sizer.Add(fsizer, flag=wx.EXPAND|wx.ALL, border=10)

        # panel.SetSizer(sizer)

        # Top Panel
        self.top_panel = MyPanel(self)

    def OnToolBarClicked(self, e):
        eid = e.GetId()
        panel:wx.Panel = None
        if eid == self.ID_TOOL_REPORT:
            panel = self.FindWindowById(self.ID_PANEL_REPORT)
        elif eid == self.ID_TOOL_PREF:
            panel = self.FindWindowById(self.ID_PANEL_PREF)

        print(panel)
        for p in self.top_panel.panels:
            p.Hide()
        panel.Show()
        self.top_panel.Layout()
        self.Fit()
        # prefDialog = PreferencesDialog(None, title='Preferences', style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        # prefDialog.ShowModal()
        # prefDialog.Destroy()

    def OnMenuClick(self, e):
        eid = e.GetId()
        print("clicked", eid)
        if eid == self.ID_MENU_PREF:
            print("pref click")
        elif eid == self.ID_MENU_EXIT:
            print("quit click")
            self.Close()

def main():
    app = MyApp()
    frm = MyFrame(None, title='Immersive Room Control', size=(640, 480))
    frm.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()