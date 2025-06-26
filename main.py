import socket
import threading


LOCAL_IP="192.168.1.100"
PORT=6969




class UDP_socket:
    def __init__(self,ip,port):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.ip = ip
        self.port = port
        self.socket.bind((self.ip,self.port))
        
    
    def send_message(self,message):
            def send_func(self,message):
                sent =self.socket.sendto(message.encode(),(self.ip,self.port))
                if sent==0:
                    raise RuntimeError("socket connection broken")
            self.send_thread= threading.Thread(target=send_func,args=(self,message))   
            self.send_thread.start()
            self.send_thread.join() 

    def listen(self):
        def listen_func(self):
            while True:    
                data, addr = self.socket.recvfrom(1024)
                print(data,addr)
        self.listen_thread = threading.Thread(target=listen_func,args=(self,))       
        self.listen_thread.start()

    def stop_listen(self):
        self.listen_thread.join()      



mySocket = UDP_socket(LOCAL_IP,PORT)

mySocket.listen()
mySocket.send_message("allo")