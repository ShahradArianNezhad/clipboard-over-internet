import os
from src.sockets import *
import time
import threading
from src.threads import *
from src.clipboard import *

PORT=6969

class TerminalProgram:

    def __init__(self):
        self.waiting_for_input=False
        self.udpSocket = UDP_socket(PORT,self)
        self.tcpSocket = TCP_socket(PORT,self)
        self.__status="polling"
        self.clipboard=ClipboardManager(self)
        self.threadPool=ThreadPool()
        self.tcpSocket.allow_requests()

    def clear_terminal(self):
        os.system('cls' if os.name=='nt' else 'clear')
    
    def set_status(self,en):
        self.__status=en

    def display_devices(self):
        self.__status = "polling"
        self.udpSocket.broadcast_message("im here!")
        self.udpSocket.listen()
        self.clear_terminal()

        def print_devices(self:TerminalProgram):
            dots=1
            while self.__status=="polling":
                while not self.waiting_for_input:
                    print("----------------Devices----------------")
                    for i in range(len(self.udpSocket.found_machines)):
                        if self.udpSocket.ip == self.udpSocket.found_machines[i]:
                            print(i+1,". ",self.udpSocket.found_machines[i],' (you)')
                        else: print(i+1,". ",self.udpSocket.found_machines[i])
                    print('searching','.'*dots)
                    if dots==3:dots=0
                    dots+=1
                    print('\n')   
                    
                    print("---------------------------------------")
                    print("enter the number of the ip you want to connect to", end=":",flush=True)
                    time.sleep(1)
                    if self.__status!="polling":break
                    self.clear_terminal()
                time.sleep(0.5)    
        self.display_thread= threading.Thread(target=print_devices,args=(self,))   
        self.display_thread.start()   
        self.get_connection_input()


    def get_connection_input(self):
        self.usrinp=0
        def getinp(self:TerminalProgram):
            self.usrinp=input("")
            if self.__status=="polling":
                try:
                    self.usrinp =int(self.usrinp)
                    if self.usrinp>len(self.udpSocket.found_machines) or self.usrinp<1:
                        raise TypeError
                except:
                    raise TypeError("enter an int inside the given range")   
                self.__status="connecting" 
                self.clear_terminal()
            if self.__status=="accept":
                pass 
            
            
        self.input_thread=threading.Thread(target=getinp,args=(self,))
        self.input_thread.start()

    def handel_connection_input(self,ip):
        self.udpSocket.stop_broadcast()
        self.udpSocket.stop_listen()
        self.udpSocket.close()

        print("waiting for response...")
        if self.tcpSocket.connect(ip):
            print("connected!")
            time.sleep(1)
            self.__status="working"


    def main(self):
        print(10000)
        self.tcpSocket.listen()  
        self.clipboard.start()
        self.tcpSocket.listen_thread.finish()




    def run(self):
        while True:
            if self.__status=="connecting":
                self.tcpSocket.block_requests()
                self.handel_connection_input(self.udpSocket.found_machines[self.usrinp-1])
            elif self.__status=="polling":
                self.display_devices()
                self.display_thread.join()   
            elif self.__status=="working":
                self.main()



        


