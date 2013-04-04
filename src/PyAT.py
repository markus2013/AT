'''
import wx, os

class TestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(TestFrame, self).__init__(*args, **kwargs)
        box = wx.BoxSizer(wx.HORIZONTAL)
        p = wx.Panel(self)
        #p.SetBackgroundColour(wx.WHITE)
        p.SetSizer(box)
        p1 = wx.Panel(p)
        #p1.SetBackgroundColour(wx.BLACK)
        p2 = wx.Panel(p)
        #p2.SetBackgroundColour(wx.RED)
        p3 = wx.Panel(p)
        #p3.SetBackgroundColour(wx.GREEN)
        box.Add(p1, 1, wx.EXPAND)
        box.Add(p2, 1, wx.EXPAND)
        box.Add(p3, 1, wx.EXPAND)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    f = TestFrame(parent=None, id=-1)
    f.Show()
    app.MainLoop()
'''
#!/usr/bin/python

# linechart.py

import wx

data = ((10, 9), (20, 22), (30, 21), (40, 30), (50, 41),
(60, 53), (70, 45), (80, 20), (90, 19), (100, 22),
(110, 42), (120, 62), (130, 43), (140, 71), (150, 89),
(160, 65), (170, 126), (180, 187), (190, 128), (200, 125),
(210, 150), (220, 129), (230, 133), (240, 134), (250, 165),
(260, 132), (270, 130), (280, 159), (290, 163), (300, 94))

years = ('2003', '2004', '2005')


class LineChart(wx.Panel): 
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.FULL_REPAINT_ON_RESIZE)
        self.SetBackgroundColour('WHITE')

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.OnResize)

        self.pre_line = None
        self.width, self.height = self.GetSize()

    def OnPaint(self, event):
        print "OnPaint" + str(self.GetSize())
        '''
        if self.pre_line is not None:
            self.DrawCursor(self.pre_line, True)
            self.pre_line = None
        '''
        dc = wx.PaintDC(self)
        self.EraseCursor()
        w, h = self.GetSize()
        dc.Clear()
        dc.SetDeviceOrigin(40, h - 40)
        dc.SetAxisOrientation(True, True)
        dc.SetPen(wx.Pen('RED'))
        dc.DrawRectangle(0, 0, w - 40, h - 40)
        self.DrawAxis(dc)
        self.DrawGrid(dc)
        self.DrawTitle(dc)
        self.DrawData(dc)
        self.pre_line = None

    def OnMotion(self, event):
        self.DrawCursor(event.GetPosition())

    def OnResize(self, event):
        print "On Resize"
        self.width, self.height = self.GetClientSize()

    def EraseCursor(self, dc=None):
        if dc is None:
            dc = wx.ClientDC(self)

        dc.SetLogicalFunction(wx.INVERT)
        dc.SetPen(wx.WHITE_PEN)

        w, h = self.GetClientSize()

        if self.pre_line:
            ox, oy = self.pre_line
            dc.DrawLine(40, oy, w, oy)
            dc.DrawLine(ox, 0, ox, h - 40)
            print "erase " + str((ox, oy))
            self.pre_line = None

    def DrawCursor(self, pos):
        x, y = pos
        dc = wx.ClientDC(self)
        w, h = self.GetClientSize()
        if y > h - 40 or x < 40:
            return

        self.EraseCursor(dc)

        dc.SetLogicalFunction(wx.INVERT)
        dc.SetPen(wx.WHITE_PEN)

        dc.DrawLine(40, y, w, y)
        dc.DrawLine(x, 0, x, h - 40)
        print "draw " + str((x, y))
        self.pre_line = (x, y)

    def DrawAxis(self, dc):
        w, h = self.GetSize()
        w -= 40
        h -= 40
        dc.SetPen(wx.Pen('#0AB1FF'))
        font =  dc.GetFont()
        font.SetPointSize(8)
        dc.SetFont(font)
        dc.DrawLine(1, 1, w, 1)
        dc.DrawLine(1, 1, 1, h)

        for i in range(1, 11):
            loc = h/11*i
            dc.DrawText(str(20*i), -30, loc+5)
            dc.DrawLine(2, loc, -5, loc)

        for i in range(3):
            loc = w/3*i
            if loc != 0:
                dc.DrawLine(loc, 2, loc, -5)
            dc.DrawText(years[i], loc-13, -10)

    def DrawGrid(self, dc):
        dc.SetPen(wx.Pen('#d5d5d5'))
        w, h = self.GetSize()
        w -= 40
        h -= 40
        for i in range(1, 11):
            loc = h/11*i
            dc.DrawLine(2, loc, w, loc)

        for i in range(1, 3):
            loc = w/3*i
            dc.DrawLine(loc, 2, loc, h)

    def DrawTitle(self, dc):
        font =  dc.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        dc.DrawText('Historical Prices', 90, 235)

    def DrawData(self, dc):
        dc.SetPen(wx.Pen('#0ab1ff'))
        w, h = self.GetSize()
        xscale = float(w-40)/(100*3)
        yscale = float(h-40)/(20*11)
        print (xscale, yscale)
        points = []
        for x,y in data:
            points.append((x*xscale, y*yscale))
        dc.DrawSpline(points)


class LineChartExample(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(390, 340))

        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('WHITE')

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        linechart = LineChart(panel)
        hbox.Add(linechart, 1, wx.EXPAND | wx.ALL, 15)
        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)


app = wx.App()
LineChartExample(None, -1, 'A line chart')
app.MainLoop()