# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------

import socket
import select
from json import loads
import asyncio

class Rester():

    OK = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
    BAD_REQUEST = 'HTTP/1.0 400 Bad Request\r\nContent-type: text/html\r\n\r\n'
    UNAUTHORIZED = 'HTTP/1.0 401 Unauthorized\r\nContent-type: text/html\r\n\r\n'
    FORBIDDEN = 'HTTP/1.0 403 Forbidden\r\nContent-type: text/html\r\n\r\n'
    NOT_FOUND = 'HTTP/1.0 404 Not Found\r\nContent-type: text/html\r\n\r\n'

    def __init__(self, daughter, host: str, port: int):
        """
        Constructs a Rester-object "api" which can be used for communicating via HTTP.
        Form of the child-class-methodes: {requestType}{url}(pathVariables || bodyVariables)

        :param daughter: object(Rester) - child-class from Rester in which the coresponding methodes to each URL are handled
        :param host: str - IPv4-Addr to be used for the socket
        :param port: int - The port number for the socket
        """
        addr = socket.getaddrinfo(host, port)[0][-1]
        self.socket = socket.socket()
        self.socket.setblocking(False)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(addr)
        self.daughter = daughter
        self.conn = None

    async def start(self) -> None:
        """
        Starts the server so it listens to new clients who want to connect.
        Infinite loop to check for new HTTP-requests.

        :return: None
        """
        self.socket.listen(1000)
        try:
            while True:
                self.check()
                await asyncio.sleep(0)
        except KeyboardInterrupt:
            pass
        
    def check_socket(self) -> bool:
        """
        Checks if a new client wants to connect to the socket.

        :return: bool - client connected
        """
        if not self.conn == None:
            return True
        try:
            self.conn, _ = self.socket.accept()
            return True
        except OSError as e:
            return False

    def check_conn(self) -> bool:
        """
        Checks if data is available at the connected socket (HTTP-request).

        :return: bool - new data available
        """
        try:
            ready_socket, _, _ = select.select([self.conn], [], [], 0)
            return ready_socket
        except OSError as e:
            return False
        
    def check_message(self) -> None:
        """
        Receives the HTTP-request and calls the corosponding methode inside the child-class.
        
        :return: None
        """
        try:
            message = self.conn.recv(1024).decode()
            request = message.split(" ")[0].lower()
        
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
            if "Content-Length:" in message:
                content_part = message.split("Content-Length:")[1]
                content_lenght = int(content_part.split("\n")[0])
                if not content_lenght == 0:
                    content_dic = loads(content_part[content_part.find("{"):])
            
            methode_name = request + url_methode_name.replace("/", "_")
            try: 
                func = getattr(self.daughter, methode_name)
                answer = func(**url_methode_parameters_dic, **content_dic)
            except:
                answer = self.BAD_REQUEST
                pass
            
            if type(answer) == str:
                self.conn.send(answer)
            elif type(answer) == tuple:
                for ans in answer:
                    self.conn.send(ans)
            else:
                raise TypeError
                
            self.conn.close()
            self.conn = None
            
        except AttributeError:
            pass
        
        except OSError:
            self.conn.close()
            self.conn = None
        
    def check(self) -> None:
        """
        Checks for new messages and processed it when there is one.
        
        :return: None
        """
        if self.check_socket():
            if self.check_conn():
                self.check_message()
    
    def close(self) -> None:
        """
        Closes the server socket connection.

        :return: None
        """
        self.socket.close()
