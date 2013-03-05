import asyncore, socket
import threading
import time, sys
import wx

import MDEvent

class MDClient(asyncore.dispatcher):
    def __init__(self, addr, win):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( addr )
        self.win = win

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        data = self.recv(8192)
        if self.win is not None:
            wx.PostEvent(self.win, MDEvent.MDEvent(data))
        else:
            print data

    def writable(self):
        return False;

    def handle_write(self):
        pass

class MDService(threading.Thread):
    def __init__(self, addr, win=None):
        threading.Thread.__init__(self)
        self.done = False
        self.client = MDClient(addr, win)

    def run(self):
        asyncore.loop()

    def stop(self):
        self.done = True

if __name__ == "__main__":
    try:
        service = MDService( ("localhost", 19999) )
        service.daemon = True
        service.start()
        while (True):
            time.sleep(1)
    except(KeyboardInterrupt, SystemExit):
        sys.exit()
