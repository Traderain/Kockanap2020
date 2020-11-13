import threading
from time import sleep
from CargameNet import CargameNet
from CargameAux import CargameAux
from CargamePrompt import CargamePrompt
from IPython import start_ipython
from traitlets.config.loader import Config
import requests
from suds.client import Client
import keyboard
from os import system
import sys
import msvcrt
import traceback
from win32api import GetKeyState
import win32api
from CargameParser import ParseTrack
from CargameListener import run

class Cargame:
    def __init__(self):
        self.thread = None
        self.net = CargameNet()
        client = Client('http://192.168.1.20:8888/DrService?wsdl')
        checkpoints = client.service.GetCheckpoints('TR0')
        print(checkpoints)
        r = requests.get("http://192.168.1.20/geekday/DRserver.php?track=TR0")
        self.track = r.text
        print('Map size:' + str(len(self.track)))
        ParseTrack(self.track, checkpoints)
        #run(addr='192.168.1.83', port='8080')

    def start(self):
        self.thread = threading.Thread(target=CargameNet.loop)
        self.thread.start()
        sleep(2)
        speed = 0x00
        angle = 0x00
        self.aux = CargameAux()
        if self.thread.isAlive():
            shouldexit = False
            while not shouldexit:
                if(self.net.response.header != 0):
                    for i in range(0, len(self.net.response.params)):
                        if self.net.response.params[i].category == 'CAR':
                            player = self.net.response.params[i].data
                            system("title Player position - X:" + str(player['X']) + " Y:" + str(player['Y']) + "Speed: " + str(speed) + "Angle: " + str(angle))
                            #if player['Player_ID'] != 0:
                            #    raise Exception('WHAT??!?!?!!?')
                        else:
                            print("what")
                try:
                    did = False
                    if win32api.GetKeyState(0x57) & 0x8000:
                        speed += 0x01
                        if speed > 0x14:
                            speed = 0x14  
                        print("Speed++")   
                        did = True                       
                    if win32api.GetKeyState(0x53) & 0x8000:
                        speed -= 0x01
                        if speed < 0x00:
                            speed = 0x00
                        print("Speed--")
                        did = True
                    if win32api.GetKeyState(0x44) & 0x8000:
                        angle += 0x01
                        if angle > 0x23:
                            angle = 0x23
                        print("Left++")
                        did = True
                    if win32api.GetKeyState(0x41) & 0x8000:
                        angle -= 0x01
                        if angle < 0x00:
                            angle = 0x00
                        print("Right++")
                        did = True
                    if did:
                        self.net.socket.sendto(CargameAux.report(self.aux, speed, angle, 0, 0),('192.168.1.20', 9999))
                        sleep(0.05)
                except IOError as e: 
                    print(e)
                    traceback.print_exc()

            self.net.close()
        else:
            print("Failed to connect to the game. Exiting...")

    def send(self, data):
        self.net.send(data)

    @staticmethod
    def configure(repl):
        repl.show_docstring = True

_main = Cargame()

def send(data):
    _main.send(data)

_main.start()