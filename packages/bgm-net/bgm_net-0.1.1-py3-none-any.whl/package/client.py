import socket
import requests
import threading
import time

class Packets:
    @staticmethod
    def Constructor(data, type: str):
        return f"{type}|".encode() + "|".join(data).encode()
    
    @staticmethod
    def Deconstructor(data: str):
        splitted = data.decode().split("|")
        return (splitted[0], splitted[1:])
    
    @staticmethod
    def connect(fromip, toip, fromport, toport):
        return Packets.Constructor([fromip, toip, str(fromport), str(toport)], "CONNECT")
    
    @staticmethod
    def disconnect(fromip, toip):
        return Packets.Constructor([fromip, toip], "DISCONNECT")
    
class Utils:
    @staticmethod
    def MyIP():
        try:
            response = requests.get("https://api.ipify.org?format=json")
            public_ip = response.json()["ip"]
            return public_ip
        except requests.RequestException as e:
            print(f"[BGM ERROR] Failed to get public ip.")
            return None

class BGM_Client:
    def __init__(self):
        self.ConnectedAddress = ()
        self.ConnectedSocket = None
        self.running = False
        
        self.ReciveCallBacks = []
        
    def connect(self, ip: str, port: int):
        address = (ip, port)
        sock =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        connect_packet = Packets.connect(Utils.MyIP(), ip, 0, port)
        
        sock.sendto(connect_packet, address)
        
        self.ConnectedAddress = address
        self.ConnectedSocket = sock
        
        self.running = True
        
        thread = threading.Thread(target=self._reciveloop)
        thread.daemon = True
        thread.start()
        
        return sock

    def _reciveloop(self):
        if self.ConnectedSocket != None:
            while self.running:
                try:
                    data, addr = self.ConnectedSocket.recvfrom(1024)
                    for callback in self.ReciveCallBacks:
                        callback(Packets.Deconstructor(data), addr)
                except Exception as e:
                    pass
        else:
            print("[BGM ERROR] Connect first to start recive loop.")

    def send(self, data, packet):
        if self.ConnectedSocket != None:
            self.ConnectedSocket.sendto(Packets.Constructor(data, packet), self.ConnectedAddress)
        else:
            print("[BGM ERROR] Connect first to use send function.")
            
    def recive_event(self, callback):
        self.ReciveCallBacks.append(callback)
        
    def disconnect(self):
        if self.ConnectedSocket != None:
            time.sleep(0.2)
            disconnect_packet = Packets.disconnect(Utils.MyIP(), self.ConnectedAddress[0])
            self.ConnectedSocket.sendto(disconnect_packet, self.ConnectedAddress)
            self.ConnectedSocket.close()
            self.ConnectedSocket = None
            
            self.running = False
        else:
            print("[BGM ERROR] Connect first to use disconnect function.")
            