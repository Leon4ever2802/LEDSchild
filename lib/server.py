# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------

import socket
import select
import struct


class Server:

    def __init__(self, host: str, port: int):
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
        self.conn = None

    def start(self) -> None:
        """
        Starts the server so it listens to new clients who want to connect

        :return: None
        """
        self.socket.listen(1000)
        
    def check_socket(self) -> bool:
        """
        Checks if a new client wants to connect to the socket

        :return: bool - new client connected
        """
        try:
            self.conn, _ = self.socket.accept()
            print("found conn:", str(self.conn))
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
            print(e)
            return False

    def accept_conn(self) -> (int, int, int):
        """
        Receives the data from the client and returns a tuple (r, g, b) with the new RGB-colors for the LED-stripe.
        Returns None if the request is bad.
        Returns (666, 666, 666, duration) if the user wants to set the LED-stripe into rainbow mode for "duration"-times

        :return: tuple (int, int, int[, int]) - new color
        """
        try:
            content = self.conn.recv(1024).decode()
            color = tuple(map(int, content.replace("\n", "").split(";")))
            print(color)
            
            if color[0] == '':
                self.conn.close()
                self.conn = None
                return None
            
            return color
        
        except ValueError as e:
            try:
                if not content.find("GET") == 0 and not content.find("HTTP") > 0:
                    raise Exception()
                
                pos = content.find("?color=")
                if pos == 5:
                    color = tuple(map(int, content.split(" ")[1][8:].split(";")))
                    print(color)
                    
                    if not len(color) == 3:
                        if len(color) == 4 and color[0] == 666 and color[1] == 666 and color[2] == 666 and color[3] > 0:
                            response = f"<!DOCTYPE html><html><head> <title>LEDSchild</title> </head><body> <h1>Farbe wurde erfolgreich ge&auml;ndert zu:</h1><h2>Rainbow Mode</h2></body></html>"
                            self.conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                            self.conn.send(response)
                            self.conn.close()
                            self.conn = None
                            return color
                        else:
                            raise Exception()
                    
                    for col in color:
                        if not 0 <= col <= 255:
                            raise Exception()
                
                    response = f"<!DOCTYPE html><html><head> <title>LEDSchild</title> </head><body> <h1>Farbe wurde erfolgreich ge&auml;ndert zu:</h1><h2>{str(color)}</h2></body></html>"
                    self.conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                    self.conn.send(response)
                    self.conn.close()
                    self.conn = None
                    return color
                else:
                    raise Exception()
            except:
                response = f"<!DOCTYPE html><html><head> <title>LEDSchild</title> </head><body> <h1>Farbe konnte nicht ge&auml;ndert werden</h1></body></html>"
                self.conn.send('HTTP/1.0 400 Bad Request\r\nContent-type: text/html\r\n\r\n')
                self.conn.send(response)
                self.conn.close()
                self.conn = None
                return None
            
        except:
            self.conn.close()
            self.conn = None
            return None
    
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
