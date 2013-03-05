import wx

EVT_MD_ID = wx.NewId()

def EVT_MD(win, func):
    win.Connect(-1, -1, EVT_MD_ID, func)

class MDEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_MD_ID)
        self.data = data

