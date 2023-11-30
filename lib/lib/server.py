import socket
import select

class Server:
    
    def __init__(self, host: str, port: int) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.conn = None
        
    def start(self) -> None:
        self.socket.listen(1)
        self.conn, _ = self.socket.accept()
        
    def check_socket(self) -> bool:
        ready_sockets, _, _ = select.select([conn], [], [], 0)
        return ready_socket
    
    def accept_socket(self) -> (int, int, int):
        return tuple(self.socket.recv(1024).decode().split(";"))