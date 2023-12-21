# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------

import socket
import select
from exceptions import SocketNotListeningError
from json import loads
import asyncio

class Rester():

    GOOD_REQUEST = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
    BAD_REQUEST = 'HTTP/1.0 400 Bad Request\r\nContent-type: text/html\r\n\r\n'

    def __init__(self, daughter, host: str, port: int):
        """
        Constructs a Server-socket to which clients can connect and change the color of the LED-stripe

        :param host: IP-Addr to be used for the socket
        :param port: The port number for the socket
        :return: Server-object
        """
        addr = socket.getaddrinfo(host, port)[0][-1]
        self.socket = socket.socket()
        self.socket.setblocking(False)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(addr)
        self.daughter = daughter
        self.conn = None

    def start(self) -> None:
        """
        Starts the server so it listens to new clients who want to connect

        :return: None
        """
        print(123)
        self.socket.listen(1000)
        self.checker()
        
    def checker(self) -> None:
        """
        """
        print(1)
        while True:
            self.check()
        
    def check_socket(self) -> bool:
        """
        Checks if a new client wants to connect to the socket

        :return: bool - new client connected
        """
        if not self.conn == None:
            return True
        try:
            self.conn, _ = self.socket.accept()
            print(self.conn)
            return True
        except OSError as e:
            return False

    def check_conn(self) -> bool:
        """
        Checks if data is available at the connected socket

        :return: bool - new data available
        """
        try:
            ready_socket, _, _ = select.select([self.conn], [], [], 0)
            return ready_socket
        except OSError as e:
            return False
        
    def check_message(self) -> None:
        """
        
        """
        try:
            message = self.conn.recv(1024).decode()
            request = message.split(" ")[0].lower()
            print(message)
            url = message.split(" ")[1].split("?")
            url_methode_name = url[0]
            
            url_methode_parameters_dic = {}
            try:
                url_methode_parameters = url[1].split("&")
                for parameter in url_methode_parameters:
                    values = parameter.split("=")
                    url_methode_parameters_dic[values[0]] = values[1]
                    
            except IndexError:
                pass
            
            content_dic = {}
            content_lenght = 0
            if "Content-Lenght:" in message:
                content_part = message.split("Content-Lenght:")[1]
                content_lenght = int(content_part.split("\n")[0])
                content_dic = loads(content_part[content_part.find("{"):])
            
            
            methode_name = request + url_methode_name.replace("/", "_")
            print(methode_name)
            func = getattr(self.daughter, methode_name)
            answer = func(**url_methode_parameters_dic, **content_dic)
            
            if type(answer) == tuple:
                for ans in answer:
                    self.conn.send(ans)
            else:
                self.conn.send(answer)
            self.conn.close()
            self.conn = None
            
        except OSError as e:
            print(e)
            self.conn.close()
            self.conn = None
        
    def check(self) -> None:
        """
        """
        if self.check_conn_isconnected():
            if self.check_conn():
                print(2)
                self.check_message()
        else:
            if self.check_socket():
                if self.check_conn():
                    self.check_message()
        
    def check_conn_isconnected(self) -> bool:
        """
        Checks whether a client is still connected or not

        :return: bool - client still connected
        """
        if self.conn == None:
            return False
        else:
            return True
    
    def close(self) -> None:
        """
        Closes the server socket connection

        :return: None
        """
        self.socket.close()
        print("closed")
