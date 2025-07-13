import os
from src.sockets import *
import time
import threading
from src.threads import *
from src.clipboard import *


class TerminalProgram:

    def __init__(self,PORT):
        self.waiting_for_input=False
        self.udpSocket = UDP_socket(PORT,self)
        self.tcpSocket = TCP_socket(PORT,self)
        self.__status="polling"
        self.clipboard=ClipboardManager(self)
        self.threadPool=ThreadPool()
        self.tcpSocket.allow_requests()

    def clear_terminal(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def shutdown(self,signum,frame):
        print('\n')
        if self.__status=="connecting":
            self.tcpSocket.client_close()
        print("press any key to shutdown")
        self.set_status("shutdown")


    
    def set_status(self,status):
        self.__status=status

    def display_devices(self):
        self.__status = "polling"
        self.udpSocket.broadcast_message("im here!")
        self.udpSocket.listen()
        self.clear_terminal()

        def print_devices(self:TerminalProgram,thread:Thread):
            while self.__status=="polling" and thread.running:
                while not self.waiting_for_input:
                    print("----------------Devices----------------")
                    for i in range(len(self.udpSocket.found_machines)):
                        if self.udpSocket.ip == self.udpSocket.found_machines[i]:
                            print(i+1,". ",self.udpSocket.found_machines[i],' (you)')
                        else: print(i+1,". ",self.udpSocket.found_machines[i])
                    print('type r to refresh')
                    print('\n')   
                    
                    print("---------------------------------------")
                    print("enter the number of the ip you want to connect to", end=":",flush=True)
                    self.get_input()
                    self.input_thread.finish()
                    if self.__status!="polling":break
                    self.clear_terminal()
                time.sleep(1)    
        self.display_thread= Thread(self,print_devices,[self]) 
        self.display_thread.start()   


    def get_input(self):
        self.usrinp=0
        def getinp(self:TerminalProgram,thread:Thread):
            self.usrinp=input("")
            if self.__status=="polling":
                if self.usrinp.lower()=="r":return 0
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
            
            
        self.input_thread=Thread(self,getinp,[self])
        self.input_thread.start()

    def handel_connection_input(self,ip):

        print("waiting for response...")
        if self.tcpSocket.connect(ip):
            self.udpSocket.stop_broadcast()
            self.udpSocket.stop_listen()
            self.udpSocket.close()
            print("connected!")
            time.sleep(1)
            self.__status="working"
        else:
            self.__status="polling"


    def main(self):
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
                self.display_thread.finish()   
            elif self.__status=="working":
                self.main()
            elif self.__status=="shutdown":
                self.clear_terminal()
                print("shutting down...")
                self.threadPool.shutdown()
                self.tcpSocket.server_close()
                self.udpSocket.close()
                break
                
            time.sleep(0.1)



        


