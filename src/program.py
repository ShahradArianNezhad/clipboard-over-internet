import os
from src.sockets import *
import time
import threading

PORT=6969

class TerminalProgram:

    def __init__(self):
        self.waiting_for_input=False
        self.udpSocket = UDP_socket(PORT)
        self.tcpSocket = TCP_socket(PORT,self)
        self.__status="None"
        self.tcpSocket.allow_requests()

    def clear_terminal(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def display_devices(self):
        if self.__status=="polling":return 0
        self.__status = "polling"
        self.udpSocket.broadcast_message("im here!")
        self.udpSocket.listen()
        self.clear_terminal()

        def print_devices(self:TerminalProgram):
            while self.__status=="polling" and not self.waiting_for_input:

                print("----------------Devices----------------")
                print('searching','...') 
                for i in range(len(self.udpSocket.found_machines)):
                    if self.udpSocket.ip == self.udpSocket.found_machines[i]:
                        print(i+1,". ",self.udpSocket.found_machines[i],' (you)')
                    else: print(i+1,". ",self.udpSocket.found_machines[i])
                print('\n')   
                
                print("---------------------------------------")
                print("enter the number of the ip you want to connect to", end=":",flush=True)
                time.sleep(1)
                if self.__status!="polling":break
                self.clear_terminal()
        self.display_thread= threading.Thread(target=print_devices,args=(self,))   
        self.display_thread.start()   
        self.get_connection_input()


    def get_connection_input(self):
        self.usrinp=0
        def getinp(self:TerminalProgram):
            self.usrinp=input("")
            try:
                self.usrinp =int(self.usrinp)
                if self.usrinp>len(self.udpSocket.found_machines) or self.usrinp<1:
                    raise TypeError
            except:
                raise TypeError("enter an int inside the given range")   
            self.__status="connecting" 
            self.clear_terminal()
            self.display_thread.join()
            

            
            
        self.input_thread=threading.Thread(target=getinp,args=(self,))
        self.input_thread.start()

    def handel_connection_input(self,ip):
        self.udpSocket.close()

        print("waiting for response...")
        if self.tcpSocket.connect(ip):
            print("allah")
        
    def run(self):
        checking = True
        def check_status(self:TerminalProgram):
            while checking:
                if self.__status=="connecting":
                    print("")
                    self.handel_connection_input(self.udpSocket.found_machines[self.usrinp-1])
                elif self.__status=="polling" or self.__status=="None":
                    self.display_devices()    
                time.sleep(1)    


        self.run_thread=threading.Thread(target=check_status,args=(self,))
        self.run_thread.run()
        
        
        
        


    def display_output(self):
        self.tcpSocket.listen()   
    def stop_display_output(self):
        self.tcpSocket.stop_listening()         



