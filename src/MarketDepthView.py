import wx
import wx.lib.agw.hypertreelist as HTL
import sys

import Network
import MDEvent

Columns = [
    "Contract",
    "BidQ",
    "Bid",
    "Ask",
    "AskQ",
    "Open",
    "High",
    "Low",
    "Close"
          ]

class MarketDepthView(HTL.HyperTreeList):
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, 
                 size = wx.DefaultSize, style=wx.SUNKEN_BORDER, 
                 agwStyle=wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_HIDE_ROOT | wx.TR_NO_LINES | wx.TR_ROW_LINES | wx.TR_COLUMN_LINES, 
                 log=None):
        HTL.HyperTreeList.__init__(self, parent, id, pos, size, style, agwStyle)

        #Create dictionary for contract item
        self.children = {} 
        self.CreateColumn()
        #self.StartMDService()

        self.GetMainWindow().Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

    def StartMDService(self):
        service = Network.MDService( ("localhost", 19999), self )
        service.daemon = True
        service.start()
        MDEvent.EVT_MD(self, self.HandleData)

    def CreateColumn(self):
        i = 0
        for item in Columns:
            self.AddColumn(item)
            self.SetColumnWidth(i, 75);
            i = i+1

        self.SetMainColumn(0);

        #This will be hidden
        self.root = self.AddRoot("DUMMY ROOT");

    def AddContract(self, name):
        if name in self.children :
            pass
        child = self.AppendItem(self.root, name)
        last = self.AppendItem(child, "")
        self.children[name] = child
        # From this point, we need to get the market info
        self.SetItemText(child, "1000", 1)
        self.SetItemText(last, "2000", 1)

    def HandleData(self, event):
        print event.data

    def OnIndicatorView(self, event):
        pass

    def OnSendOrder(self, event):
        pass

    def OnClosePosition(self, event):
        pass

    def OnStartStrategy(self, event):
        pass

    def OnStopStrategy(self, event):
        pass

    def OnStopAllStrategy(self, event):
        pass

    def OnOpenOrderBook(self, event):
        pass

    def OnContextMenu(self, event):
        print "context menu"

    def OnRightDown(self, event):
        print "click down"

        pt = event.GetPosition()
        item, flags, column = self.HitTest(pt)

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

        enable = item is not None;

        menu = wx.Menu()
        menu.Append(self.popupID1, "Open Indicator View").Enable(enable)
        menu.AppendSeparator()
        menu.Append(self.popupID2, "Send Order").Enable(enable)
        menu.Append(self.popupID3, "Close Position").Enable(enable)
        menu.AppendSeparator()
        menu.Append(self.popupID4, "Start Strategy").Enable(enable)
        menu.Append(self.popupID5, "Stop Strategy").Enable(enable)
        menu.Append(self.popupID6, "Stop All Strategies").Enable(enable)
        menu.AppendSeparator()
        menu.Append(self.popupID7, "Open Order Book").Enable(enable)

        self.PopupMenu(menu)
        menu.Destroy()


if __name__ == "__main__":
    try:
        app = wx.PySimpleApp()
        frame = wx.Frame(None, -1, "Test")
        view = MarketDepthView(frame)
        view.AddContract("Gold")
        view.AddContract("Silver")
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(view, 1, wx.EXPAND)
        frame.SetSizer(vbox)
        frame.Show()
        app.MainLoop()
    except(KeyboardInterrupt, SystemExit):
        sys.exit()
