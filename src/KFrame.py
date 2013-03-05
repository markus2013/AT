import matplotlib
matplotlib.use('WXAgg')
import pylab
import matplotlib.dates
import matplotlib.finance
import matplotlib.backends.backend_wxagg as wxagg
import matplotlib.widgets
 
import wx
import datetime

'''
date1 = (2004, 2, 1)
date2 = (2004, 4, 12)

mondays = matplotlib.dates.WeekdayLocator(matplotlib.dates.MONDAY)
alldays = matplotlib.dates.DayLocator()
weekFormatter = matplotlib.dates.DateFormatter('%b %d')
dayFormatter = matplotlib.dates.DateFormatter('%d')

quotes = matplotlib.finance.quotes_historical_yahoo('INTC', date1, date2)
if len(quotes) == 0:
    raise SystemExit

fig = pylab.figure()
fig.subplots_adjust(bottom = 0.2)
ax = fig.add_subplot(111)
ax.xaxis.set_major_locator(mondays)
ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(weekFormatter)

matplotlib.finance.candlestick(ax, quotes, width=0.6)
ax.xaxis_date()
ax.autoscale_view()
pylab.setp(pylab.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
pylab.show()
'''
class Cursor:
    def __init__(self, ax, canvas):
        self.ax = ax
        self.canvas = canvas
        self.lx = ax.axhline(y = ax.get_ylim()[0], color='k')  # the horiz line
        self.ly = ax.axvline(x = ax.get_xlim()[0], color='k')  # the vert line

        # text location in axes coords
        self.txt = ax.text( 0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes: return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y )
        self.ly.set_xdata(x )

        self.txt.set_text( 'x=%1.2f, y=%1.2f'%(x,y) )
        self.canvas.draw()
        pass

class KFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Demo")
        self.create_panel()
       
    def create_panel(self):
        self.panel = wx.Panel(self)
        
        self.create_plot()
        
        self.canvas = wxagg.FigureCanvasWxAgg(self.panel, -1, self.fig)

        self.cursor = matplotlib.widgets.Cursor(self.ax)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW, border=0)        
        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

        self.canvas.draw()
        
    def create_plot(self):
        self.fig = pylab.figure()
        self.fig.subplots_adjust(bottom = 0.2)
        
        '''
        self.date1 = datetime.date(2004, 2, 1)
        self.date2 = datetime.date(2004, 4, 12)

        self.mondays = matplotlib.dates.WeekdayLocator(matplotlib.dates.MONDAY)
        self.alldays = matplotlib.dates.DayLocator()
        self.weekFormatter = matplotlib.dates.DateFormatter('%b %d')
        self.dayFormatter = matplotlib.dates.DateFormatter('%d')

        self.quotes = matplotlib.finance.quotes_historical_yahoo('INTC', self.date1, self.date2)
        if len(self.quotes) == 0:
            raise SystemExit

        self.ax = self.fig.add_subplot(111)
        self.ax.xaxis.set_major_locator(self.mondays)
        self.ax.xaxis.set_minor_locator(self.alldays)
        self.ax.xaxis.set_major_formatter(self.weekFormatter)
        matplotlib.finance.candlestick(self.ax, self.quotes, width=0.6)
        self.ax.xaxis_date()
        self.ax.autoscale_view()
        pylab.setp(pylab.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
        '''
        self.hours = matplotlib.dates.HourLocator()
        self.mins  = matplotlib.dates.MinuteLocator(byminute=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        self.date1 = datetime.date(2004, 2, 1)
        self.date2 = datetime.date(2004, 4, 12)
        self.timeFormatter = matplotlib.dates.DateFormatter('%H:%M:%S')
        self.quotes = []
        self.time = datetime.datetime(2004, 2, 1, 12, 20, 0)
        self.delta = datetime.timedelta(minutes=5)
        for d, o, c, h, l, v in matplotlib.finance.quotes_historical_yahoo('INTC', self.date1, self.date2):
            self.quotes.append((matplotlib.dates.date2num(self.time), o, c, h, l, v))
            self.time = self.time + self.delta

        self.ax = self.fig.add_subplot(111)
        self.ax.xaxis.set_major_locator(self.hours)
        self.ax.xaxis.set_minor_locator(self.mins)
        self.ax.xaxis.set_major_formatter(self.timeFormatter)
        matplotlib.finance.candlestick(self.ax, self.quotes, width=0.002)
        self.ax.autoscale_view()
        pylab.setp(pylab.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
 

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = KFrame(None)
    frame.Show()
    app.MainLoop()
