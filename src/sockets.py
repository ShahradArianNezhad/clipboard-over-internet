import socket
import threading
import time
from src.threads import *

class UDP_socket:
    def __init__(self,port,program):
        self.program = program
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.ip = self.get_ip()
        self.port = port
        self.socket.bind(('0.0.0.0',self.port))
        self.found_machines=list()
        self.__is_connected=False



        print(f"listening on port {self.port}")
        
    
    def get_ip(self):
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as mySocket:
            try:    
                mySocket.connect(("8.8.8.8",80))
                return mySocket.getsockname()[0]
            except socket.error:
                raise RuntimeError("GetLocalIP failed (couldnt connect to 8.8.8.8)")
            finally:
                mySocket.close()



    def broadcast_message(self,message:str):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            def send_func(self:UDP_socket,message,thread:Thread):
                while thread.running:
                    time.sleep(1)
                    if thread.running==False:break
                    sent =self.socket.sendto(message.encode(),('192.168.1.255',self.port))
                    if sent==0:
                        raise RuntimeError("socket connection broken")
                
            self.send_thread=Thread(self.program,send_func,[self,message])
            self.send_thread.start()

    def stop_broadcast(self):
        self.send_thread.stop()



    def listen(self):
        def listen_func(self:UDP_socket,thread:Thread):
            while thread.running:    
                data, addr = self.socket.recvfrom(1024)
                if addr[0] not in self.found_machines : self.found_machines.append(addr[0])
        self.listen_thread = Thread(self.program,listen_func,[self])      
        self.listen_thread.start()

    def stop_listen(self):
        self.listen_thread.stop()

    def close(self):
        self.socket.close()        


class TCP_socket:
    def __init__(self,port,program):
        self.program = program
        self.__acting_as="None"
        self.server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port=port
        self.server_socket.bind(('0.0.0.0',self.port))
        self.connections=list()

    def connect(self,host):
        self.client_socket.connect((host,self.port))
        data = self.client_socket.recv(1024).decode()
        if data=="declined":
            print("access declined")
            return False
        elif data=="accepted":
            self.connected_to=host
            self.__is_connected=True
            print(f"connected to {host}")
            self.__acting_as="client"
            return True

              
        
        

    def send_message(self,message:str):
        if self.__is_connected:
            if self.__acting_as=="client":
                try:
                    self.client_socket.sendall(message.encode())
                    print(f"sent {message} to {self.connected_to}")
                except Exception:
                    raise RuntimeError(f"couldnt send message through tcp to {self.connected_to}")    
            elif self.__acting_as=="server":
                self.connections[0].sendall(message.encode())   


    def listen(self):
        if self.__acting_as=="client":
            def listen_func(self:TCP_socket,thread:Thread):
                while thread.running:
                    data = self.client_socket.recv(1024)
                    if thread.running==False:return 0
                    print("recieved: ",data.decode())
                    self.program.clipboard.copy_to_clipboard(data.decode())
        elif self.__acting_as=="server":
            def listen_func(self:TCP_socket,thread:Thread):
                while thread.running:
                    data = self.connections[0].recv(1024)
                    if thread.running==False:return 0
                    print("recieved: ",data.decode())
                    self.program.clipboard.copy_to_clipboard(data.decode())

        self.listen_thread = Thread(self.program,listen_func,[self])  
        self.listen_thread.start()

    def stop_listening(self):
        self.listen_thread.stop()

    def client_close(self):
        self.client_socket.close()        
    def server_close(self):
        self.server_socket.close()

    def allow_requests(self):
        self.server_socket.listen(3)
        def handler_func(self:TCP_socket,thread:Thread):
            try:
                while thread.running:
                    connection,addr=self.server_socket.accept()  
                    self.program.waiting_for_input=True 
                    self.program.set_status("accept")
                    time.sleep(2)
                    self.program.clear_terminal()
                    print(f"Recieved a request from {addr}, accept?(y/n)")
                    self.program.input_thread.join()
                    print(self.program.usrinp)
                    usr_inp=self.program.usrinp
                    if usr_inp.lower()=='n':
                        connection.sendall("declined".encode())
                        connection.close()
                        self.program.waiting_for_input=False
                    elif usr_inp.lower()=='y':
                        self.__acting_as="server"
                        connection.sendall("accepted".encode())
                        self.connections.append(connection)
                        self.__is_connected=True
                        self.connected_to=addr
                        print("connected successfuly")
                        self.program.set_status("working")
                        self.program.waiting_for_input=False
                    else:
                        raise Exception
                            
            except Exception:
                raise RuntimeError("Error in accepting")
        self.accepting_thread=Thread(self.program,handler_func,[self])
        self.accepting_thread.start()

    def block_requests(self):
        self.accepting_thread.stop()

                