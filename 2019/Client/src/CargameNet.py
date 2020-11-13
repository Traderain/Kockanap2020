import asyncore, socket
from CargameResponse import ResponseParser
from time import sleep

class CargameNet(asyncore.dispatcher_with_send):
    def __init__(self):
        asyncore.dispatcher_with_send.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind(('192.168.1.61', 1234))
        self.isClosing = False

    def handle_connect(self):
        print("Connected!")
        pass

    def handle_write(self):
        pass

    def handle_read(self):
        data = self.recv(8192*32)
        try:
            self.response = ResponseParser.parse(data)
        except:
            print("Mallformed packet!")
            

    def reconnect(self):
        self.bind(('192.168.1.61', 1234))
    
    @staticmethod
    def loop():
        asyncore.loop()