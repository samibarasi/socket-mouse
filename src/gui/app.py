import wx

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

class MyApp(wx.App):
    def OnInit(self):
        return super().OnInit()

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
        tb.Bind(wx.EVT_TOOL, self.OnChangeList)

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
        panel = wx.Panel(self, self.ID_PANEL_REPORT)
        resolutionLabel = wx.StaticText(panel, label="Resolution:")
        resolutionValue = wx.StaticText(panel, self.ID_RESOLUTION, label="N/A")
        dpiLabel = wx.StaticText(panel, label="DPI:")
        dpiValue = wx.StaticText(panel, self.ID_DPI, label="N/A")

        sizer = wx.BoxSizer(wx.VERTICAL)

        fsizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        fsizer.Add(resolutionLabel, 1, wx.ALIGN_RIGHT)
        fsizer.Add(resolutionValue, 1)
        fsizer.Add(dpiLabel, 1, wx.ALIGN_RIGHT)
        fsizer.Add(dpiValue, 1)

        sizer.Add(fsizer, flag=wx.EXPAND|wx.ALL, border=10)

        panel.SetSizer(sizer)

    def OnChangeList(self, e):
        eid = e.GetId()
        panel = None
        if eid == self.ID_TOOL_REPORT:
            panel = self.FindWindowById(self.ID_PANEL_REPORT)
        elif eid == self.ID_TOOL_PREF:
            panel = self.FindWindowById(self.ID_PANEL_PREF)

        print(panel)
        prefDialog = PreferencesDialog(None, title='Preferences', style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        prefDialog.ShowModal()
        prefDialog.Destroy()

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
    frm = MyFrame(None, title='Immersive Room Control')
    frm.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()