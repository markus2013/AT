import asyncore, socket
import threading
import time
import sys

class Client(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.stopme = False

    def run(self):
        while not self.stopme:
                try:
                    time.sleep(1)
                    self.sock.send("hello there\n");
                except:
                    print "connection closed"
                    self.stop()

    def stop(self):
        self.stopme = True


class MockServer(asyncore.dispatcher):
    def __init__(self) :
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind( ("localhost", 19999) )
        self.listen(10)
        self.clients = {}

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            client = Client(sock)
            client.daemon = True
            self.clients[addr] = client
            client.start()


if __name__ == "__main__":
    try:
        mock = MockServer()
        asyncore.loop(1)
    except(KeyboardInterrupt, SystemExit):
        sys.exit()

