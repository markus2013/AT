import wx
import os

from MarketDepthView import *
from Dialogs import *

ADM_LOGIN_ID = wx.NewId()
ADM_LOGOUT_ID = wx.NewId()
ADM_EXIT_ID = wx.NewId()
CTR_ADD_ID = wx.NewId()
VIW_MKTDPT_ID = wx.NewId()
VIW_IND_ID = wx.NewId()

class PricingView(wx.Frame) :
    def __init__(self, name) :
        wx.Frame.__init__(self, None, -1, name, size=(640,480))

        # create menu 
        self.CreateMenu()

        # create the tool bar, optional
        # create_toolbar()

        # create the status bar
        self.CreateStatusbar()

        # Brief layout
        self.InitLayout()

    def InitLayout(self) :
        self.hsplitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN|wx.SP_LIVE_UPDATE|wx.SP_3D)
        self.upnl = wx.Panel(self.hsplitter, -1)
        self.upnl.SetBackgroundColour(wx.RED)
        self.dpnl  = wx.Panel(self.hsplitter, -1)
        self.dpnl.SetBackgroundColour(wx.GREEN)
        self.hsplitter.SplitHorizontally(self.upnl, self.dpnl, -1)
        self.hsplitter.Unsplit(self.dpnl)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.hsplitter, 1, wx.EXPAND)
        self.SetSizer(self.vbox)
        self.Centre()

        self.vsplitter = wx.SplitterWindow(self.upnl, -1)
        self.lpnl = wx.Panel(self.vsplitter, -1)
        self.lpnl.SetBackgroundColour(wx.WHITE)
        self.rpnl = wx.Panel(self.vsplitter, -1)
        self.rpnl.SetBackgroundColour(wx.BLACK)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vsplitter.SplitVertically(self.lpnl, self.rpnl, 1)
        self.vsplitter.Unsplit(self.lpnl)
        self.hbox.Add(self.vsplitter, 1, wx.EXPAND)
        self.upnl.SetSizer(self.hbox)

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.mdv = MarketDepthView(self.rpnl)
        vbox.Add(self.mdv, -1, wx.EXPAND)
        self.rpnl.SetSizer(vbox)

        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

    def CreateMenu(self):
        '''Admin Menu'''
        admmenu = wx.Menu()
        admmenu.Append(ADM_LOGIN_ID, "&Login")
        admmenu.Append(ADM_LOGOUT_ID, "&Logout")
        admmenu.Append(ADM_EXIT_ID, "&Exit")
        self.Bind(wx.EVT_MENU, self.OnAdminLogin, id=ADM_LOGIN_ID)
        self.Bind(wx.EVT_MENU, self.OnAdminLogout, id=ADM_LOGOUT_ID)
        self.Bind(wx.EVT_MENU, self.OnAdminExit, id=ADM_EXIT_ID)

        '''Contract Menu'''
        ctrmenu = wx.Menu()
        ctrmenu.Append(CTR_ADD_ID, "&Add Contract")
        self.Bind(wx.EVT_MENU, self.OnAddContract, id=CTR_ADD_ID)

        '''View Menu'''
        viewmenu = wx.Menu()
        viewmenu.Append(VIW_IND_ID, "&Indicator View")
        self.Bind(wx.EVT_MENU, self.OnIndicatorView, id=VIW_IND_ID)

        '''The menu bar'''
        menubar = wx.MenuBar()
        menubar.Append(admmenu, "&Admin")
        menubar.Append(ctrmenu, "&Contract")
        menubar.Append(viewmenu, "&View")
        self.SetMenuBar(menubar)
        pass

    def CreateToolbar(self):
        pass

    def CreateStatusbar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusText("No Status", 0)
        self.statusbar.SetStatusText("No Connection", 0)
        pass

    def OnAddContract(self, event):
        selector = CtrSelector(self, -1)
        selector.ShowModal()
        selector.Destroy()
        for ctr in selector.GetSelected():
            self.mdv.AddContract(ctr)
        pass

    def OnDelContract(self, event):
        pass

    def OnAdminLogin(self, event):
        login = LoginDialog(self, -1)
        val = login.ShowModal()
        login.Destroy()
        pass

    def OnAdminLogout(self, event):
        '''Should call logout'''
        pass

    def OnAdminExit(self, event):
        '''Should check status and potentially close connections'''
        self.Close()
        pass

    def OnIndicatorView(self, event):
        if event.GetId() == VIW_IND_ID:
            selector = CtrSelector(self, -1)
            selector.ShowModal()
            selector.Destroy()
            items = selector.GetSelected()

    def OnRightClick(self, event):
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            self.popupID6 = wx.NewId()
            self.popupID7 = wx.NewId()

        self.Bind(wx.EVT_MENU, self.OnIndicatorView, id=self.popupID1)
        self.Bind(wx.EVT_MENU, self.OnSendOrder, id=self.popupID2)
        self.Bind(wx.EVT_MENU, self.OnClosePosition, id=self.popupID3)
        self.Bind(wx.EVT_MENU, self.OnStartStrategy, id=self.popupID4)
        self.Bind(wx.EVT_MENU, self.OnStopStrategy, id=self.popupID5)
        self.Bind(wx.EVT_MENU, self.OnStopAllStrategy, id=self.popupID6)
        self.Bind(wx.EVT_MENU, self.OnOpenOrderBook, id=self.popupID7)

        menu = wx.Menu()
        menu.Append(self.popupID1, "Open Indicator View")
        menu.Append(self.popupID2, "Send Order")
        menu.Append(self.popupID3, "Close Position")
        menu.Append(self.popupID4, "Start Strategies")
        menu.Append(self.popupID5, "Stop Strategy")
        menu.Append(self.popupID6, "Stop All Strategies")
        menu.Append(self.popupID7, "Open Order Book")

        self.PopupMenu(menu)
        menu.Destroy()

        pass

    def OnRightDown(self, event):
        print "Right Click"

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = PricingView("PricingView")
    frame.Show()
    app.MainLoop()
