import socket
import configparser

class Connection:
    def __init__(self,inifile:configparser.ConfigParser) -> None:
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.buffer = inifile.getint("connection","buffer")
    
    def receive(self, socket:socket.socket) -> str:
        responses = b""

        while not self.is_json_complate(responces=responses):
            response = socket.recv(self.buffer)
            
            if response == b"":
                raise RuntimeError("socket connection broken")
            
            responses += response

        return responses.decode("utf-8")
    
    def send(self, socket:socket.socket, message:str) -> None:
        message += "\n"

        socket.send(message.encode("utf-8"))
    
    def close(self) -> None:
        self.socket.close()
    
    def is_json_complate(responces:bytes) -> bool:
        try:
            responces = responces.decode("utf-8")
        except:
            return False
        
        if responces == "":
            return False
        
        cnt = 0

        for word in responces:
            if word == "{":
                cnt += 1
            elif word == "}":
                cnt -= 1
        
        return cnt == 0

class TCPClient(Connection):

    def __init__(self, inifile:configparser.ConfigParser) -> None:
        super().__init__(inifile=inifile)
        self.host = inifile.get("tcp-client","host")
        self.port = inifile.getint("tcp-client","port")

    def connect(self) -> None:
        self.socket.connect((self.host,self.port))
    
    def receive(self) -> str:
        return super().receive(socket=self.socket)
    
    def send(self, message:str) -> None:
        super().send(socket=self.socket, message=message)

    def close(self) -> None:
        super().close()