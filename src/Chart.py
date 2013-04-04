import wx

class Chart(wx.Panel):
    """description of class"""
    def __init__(self, parent):
        wx.Panel(parent, -1, style=wx.FULL_REPAINT_ON_RESIZE)

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = wx.Frame(None, -1, "Hello")
    chart = Chart(frame)
    frame.Show()
    app.MainLoop()