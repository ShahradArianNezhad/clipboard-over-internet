import os
from src.sockets import *
import time
import threading

PORT=6969

class TerminalProgram:

    def __init__(self):
        self.udpSocket = UDP_socket(PORT)
        self.tcpSocket = TCP_socket(PORT)
        self.__polling=False

    def clear_terminal(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def display_devices(self):
        self.__polling=True
        self.udpSocket.broadcast_message("im here!")
        self.udpSocket.listen()
        def print_devices(self:TerminalProgram,dots):
            while self.__polling:
                time.sleep(1)
                print("----------------Devices----------------")
                for i in range(len(self.udpSocket.found_machines)):
                    print(i+1,". ",self.udpSocket.found_machines[i])
                print('\n')   
                if dots==3:dots=1
                print('searching','.'*dots) 
                print("---------------------------------------")
                self.clear_terminal()
        self.display_thread= threading.Thread(target=print_devices,args=(self,1,))     
        self.display_thread.start()   

    def stop_displaying_devices(self):
        if self.__polling:
            self.__polling:False
            self.display_thread.join


    def display_output(self):
        self.tcpSocket.listen()   
    def stop_display_output(self):
        self.tcpSocket.stop_listening()         



