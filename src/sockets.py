import socket
import threading
import time

class UDP_socket:
    def __init__(self,port):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.ip = self.get_ip()
        self.port = port
        self.socket.bind(('0.0.0.0',self.port))
        self.__listening=False
        self.__broadcasting=False
        self.found_machines=list()



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
            self.__broadcasting=True
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            def send_func(self:UDP_socket,message):
                while self.__broadcasting:
                    time.sleep(1)
                    sent =self.socket.sendto(message.encode(),('192.168.1.255',self.port))
                    if sent==0:
                        raise RuntimeError("socket connection broken")
                
            self.send_thread= threading.Thread(target=send_func,args=(self,message))   
            self.send_thread.start()

    def stop_broadcast(self):
        self.__broadcasting=False
        self.send_thread.join()



    def listen(self):
        self.__listening=True
        def listen_func(self:UDP_socket):
            while self.__listening:    
                data, addr = self.socket.recvfrom(1024)
                if addr[0]!=self.ip : self.found_machines.append(addr[0])
        self.listen_thread = threading.Thread(target=listen_func,args=(self,))       
        self.listen_thread.start()

    def stop_listen(self):
        if self.__listening:
            self.__listening = False
            self.listen_thread.join() 

    def close(self):
        self.socket.close()        


class TCP_socket:
    def __init__(self,port,program):
        self.program = program
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port=port
        self.socket.bind(('0.0.0.0',self.port))
        self.__listening=False
        self.__accepting=False
        self.connections=list()

    def connect(self,host):
        
        try:
            self.socket.connect((host,self.port))
            print(f"connected to {host}:{self.port}")
        except:
            raise RuntimeError("connection failed")    
        
        self.connected_to=host
        self.__is_connected=True

    def send_message(self,message:str):
        if self.__is_connected:
            try:
                self.socket.sendall(message.encode())
                print(f"sent {message} to {self.connected_to}")
            except Exception:
                raise RuntimeError(f"couldnt send message through tcp to {self.connected_to}")    
        else:
            print("not connected to send any messages!")    

    def listen(self):
        self.__listening=True
        def listen_func(self:TCP_socket):
            while self.__listening:
                data = self.socket.recv(1024)
                print(data.decode())
        self.listen_thread = threading.Thread(target=listen_func,args=(self,))        
        self.listen_thread.start()

    def stop_listening(self):
        if self.__listening:
            self.__listening=False
            self.listen_thread.join()    

    def close(self):
        self.socket.close()        


    def allow_requests(self):
        self.__accepting=True
        self.socket.listen(3)
        def handler_func(self:TCP_socket):
            try:
                while self.__accepting:
                    connection,addr=self.socket.accept()  
                    self.program.waiting_for_input=True 
                    print(f"Recieved a request from {addr}, accept?(y/n)")
                    usr_inp=input("")
                    if usr_inp.lower()=='n':
                        connection.close()
                        self.program.waiting_for_input=False
                    if usr_inp.lower()=='y':
                        self.connections.append(connection)
                        print("connected successfuly")
                        self.program.waiting_for_input=False
            except Exception:
                raise RuntimeError("Error in accepting")
        self.accepting_thread=threading.Thread(target=handler_func,args=(self,))    
        self.accepting_thread.start()

    def block_requests(self):
        if self.__accepting:
            self.__accepting=False
            self.accepting_thread.join()
                