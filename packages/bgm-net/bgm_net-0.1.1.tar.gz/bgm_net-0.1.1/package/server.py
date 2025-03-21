import socket

class Packets:
    @staticmethod
    def Constructor(data, type: str):
        return f"{type}|".encode() + "|".join(data).encode()
    
    @staticmethod
    def Deconstructor(data: str):
        splitted = data.decode().split("|")
        return (splitted[0], splitted[1:])

class BGM_Server:
    def __init__(self, host, port):
        self.Address = (host, port)
        self.Sock = None
        
        self.Clients = []
        
        self.ReciveCallBacks = []
        self.ConnectCallBacks = []
        self.DisconnectCallBacks = []
    
    def recive_event(self, callback):
        self.ReciveCallBacks.append(callback)
    
    def connect_event(self, callback):
        self.ConnectCallBacks.append(callback)
        
    def disconnect_event(self, callback):
        self.DisconnectCallBacks.append(callback)
    
    def start_server(self):
        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Sock.bind(self.Address)
        
        print(f"Server on {self.Address[0]}:{self.Address[1]}")
        
        while True:
            try:
                message, client_address = self.Sock.recvfrom(1024)
                
                message = Packets.Deconstructor(message)

                if message[0] == "CONNECT":
                    self.Clients.append(client_address)
                    for callback in self.ConnectCallBacks:
                        callback(client_address)
                elif message[0] == "DISCONNECT":
                    self.Clients.remove(client_address)
                    for callback in self.DisconnectCallBacks:
                        callback(client_address)
                else:
                    for callback in self.ReciveCallBacks:
                        callback(message, client_address)
            except:
                pass
                
    def broadcast(self, message):
        for client in self.Clients:
            self.Sock.sendto(message, client)
