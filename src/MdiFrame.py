import wx
from KFrame import KFrame

class MdiFrame(wx.MDIParentFrame):
    def __init__(self):
        wx.MDIParentFrame.__init__(self, None, -1, "MDI Parent", size=(600, 400))
        
        self.create_menu()
        self.create_toolbar()
        
    def create_menu(self):
        self.menu = wx.Menu()
        self.menu.Append(5000, "&New Window")
        self.menu.Append(5001, "E&xit")
        self.menubar = wx.MenuBar()
        self.menubar.Append(self.menu, "&File")
        self.SetMenuBar(self.menubar)
        self.Bind(wx.EVT_MENU, self.on_new_window, id=5000)
        self.Bind(wx.EVT_MENU, self.on_exit, id=5001)
    
    def create_toolbar(self):
        pass
    
    def on_new_window(self, evt):
        win = KFrame(self)
        win.Show()
    
    def on_exit(self, evt):
        self.Close(True)
        
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = MdiFrame()
    frame.Show()
    app.MainLoop()
