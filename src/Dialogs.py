import wx, sys

class CtrSelectorPanel(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        self.InitPanel()

        self.selected = list()

    def InitPanel(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.lst = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
        self.PopulateList()
        vbox.Add(self.lst, 1, wx.EXPAND)
        self.SetSizer(vbox)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSeleted, self.lst)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.lst)

    def PopulateList(self):
        self.lst.InsertColumn(0, "Name")
        self.lst.InsertColumn(0, "Type")
        
        for i in range(50):
            index = self.lst.InsertStringItem(sys.maxint, "GOLD" + str(i))
            self.lst.SetStringItem(index, 1, "Future")

        index = self.lst.InsertStringItem(sys.maxint, "OIL")
        self.lst.SetStringItem(index, 1, "Future")

    def OnItemSeleted(self, evt):
        print evt.m_itemIndex
        print "Select " + self.lst.GetItem(evt.m_itemIndex, 0).GetText()
        selected = self.lst.GetItem(evt.m_itemIndex, 0).GetText()
        if (selected not in self.selected):
            self.selected.append(selected)
        pass

    def OnItemDeselected(self, evt):
        print evt.m_itemIndex
        print "Deselect " + self.lst.GetItem(evt.m_itemIndex, 0).GetText()
        deselected = self.lst.GetItem(evt.m_itemIndex, 0).GetText()
        if (deselected in self.selected):
            self.selected.remove(deselected)
        pass


class CtrSelector(wx.Dialog):
    def __init__(self, *args, **kw):
        wx.Dialog.__init__(self, *args, **kw)

        self.InitLayout()
        self.SetTitle("Contract Selector")

    def InitLayout(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.pnl = CtrSelectorPanel(self)
        vbox.Add(self.pnl, 1, wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 20)

        btnbox = wx.StdDialogButtonSizer()
        okButton = wx.Button(self, id=wx.ID_OK)
        clButton = wx.Button(self, id=wx.ID_CANCEL)
        btnbox.Add(okButton)
        btnbox.Add(clButton)
        btnbox.Realize()

        vbox.Add(btnbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

    def GetSelected(self):
        if (self.pnl is not None and self.pnl.selected is not None):
            return self.pnl.selected
        else:
            pass

    def OnOk(self, evt):
        self.Close()
        pass

    def OnClose(self, evt):
        self.pnl.selected = list()
        self.Close()
        pass


class LoginDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        wx.Dialog.__init__(self, *args, **kw)
        self.SetSize((200,200))
        self.SetTitle("Login Infomation");

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        label1 = wx.StaticText(self, -1, "User:", style=wx.ALIGN_RIGHT);
        label2 = wx.StaticText(self, -1, "Password:", style=wx.ALIGN_RIGHT);
        label3 = wx.StaticText(self, -1, "Host:", style=wx.ALIGN_RIGHT);
        vbox1.Add(label1, 0, wx.ALIGN_RIGHT|wx.ALL, 10)
        vbox1.Add(label2, 0, wx.ALIGN_RIGHT|wx.ALL, 10)
        vbox1.Add(label3, 0, wx.ALIGN_RIGHT|wx.ALL, 10)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        self.text1 = wx.TextCtrl(self, -1, "")
        self.text2 = wx.TextCtrl(self, -1, "");
        self.text3 = wx.TextCtrl(self, -1, "");
        vbox2.Add(self.text1, 1, wx.ALIGN_LEFT|wx.ALL, 5)
        vbox2.Add(self.text2, 1, wx.ALIGN_LEFT|wx.ALL, 5)
        vbox2.Add(self.text3, 1, wx.ALIGN_LEFT|wx.ALL, 5)

        hbox.Add(vbox1, 0, wx.ALIGN_CENTRE|wx.ALL)
        hbox.Add(vbox2, 1, wx.ALIGN_CENTRE|wx.ALL)

        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox3.Add(hbox, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        btnbox = wx.StdDialogButtonSizer()
        okButton = wx.Button(self, id=wx.ID_OK)
        clButton = wx.Button(self, id=wx.ID_CANCEL)
        btnbox.Add(okButton)
        btnbox.Add(clButton)
        btnbox.Realize()
 
        vbox3.Add(btnbox, 0, wx.ALIGN_CENTRE|wx.ALL, 15)

        self.SetSizer(vbox3)

if __name__ == "__main__":
    try:
        app = wx.PySimpleApp()
        selector = CtrSelector(None, -1)
        selector.ShowModal()
        selector.Destroy()
        print selector.GetSelected()
        login = LoginDialog(None, -1)
        val = login.ShowModal()
        print val
        if val == wx.ID_OK:
            print login.text1.GetValue() + ":" + login.text2.GetValue() + ":" + login.text3.GetValue()
        login.Destroy()
    except(KeyboardInterrupt, SystemExit):
        sys.exit()
