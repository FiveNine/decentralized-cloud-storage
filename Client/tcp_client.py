import socket
import pickle
# from utils import *
from typing import TypeVar
T = TypeVar('T')

class Client:
    def __init__(self, server_address : tuple[str, int]) -> socket.socket:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock.bind(('0.0.0.0', 59590))

        self.relay_server_address = server_address


    def __accept(self) -> None:
        print(f"Accepting connection on port 59590.")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.bind(('0.0.0.0', 59590))
        sock.listen(1)
        sock.settimeout(5)

        while not self.CONNECTION_ESTABLISHED.is_set():
            try:
                connection, address = sock.accept()
            except socket.timeout:
                continue
            else:
                print("Connection Accepted! This is host.")
                self.CONNECTION_ESTABLISHED.set()
                self.sock = sock
                
    def __connect(self, address: tuple[str, int]) -> None:
        print(f"Connecting from {('0.0.0.0', 59590)} to {address}.")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.bind(('0.0.0.0', 59590))

        connection_established = False
        while not connection_established:
            try:
                sock.connect(address)
            except socket.error:
                continue
            else:
                print("Connection Established!")
                connection_established = True
                return sock
    
    def join_queue(self) -> None:
        self.sock = self.__connect(self.relay_server_address)
        # wait until relay server finds a client
        self.send_message("Host")
        other_address = self.receive_message()
        print(f"Server sent client: {other_address}")
        self.sock = self.__connect(other_address)
    
    def find_host(self) -> None:
        self.sock = self.__connect(self.relay_server_address)
        # relay server finds appropriate host and sends address
        self.send_message("Client")
        other_address = self.receive_message(self.sock)
        print(f"Server sent client: {other_address}")
        self.sock = self.__connect(other_address)

    def send_message(self, message: T) -> None:
        raw_data = pickle.dumps(message)
        data_length = len(raw_data).to_bytes(4, byteorder='big')
        self.sock.sendall(data_length)

        self.sock.sendall(raw_data)

    def receive_message(self) -> T:

        # receive message length in bytes
        data_length = self.sock.recv(4)
        
        # convert message length to int
        data_length = int.from_bytes(data_length, byteorder='big')

        # receive message with a buffer of 4KB
        message = ''
        received_bytes = 0
        while received_bytes < data_length:
            remaining = data_length - received_bytes
            message += self.sock.recv(remaining if remaining < 4096 else 4096)
            received_bytes = len(message)

        return pickle.loads(message)

    # def send_file(self, file_path: str) -> None:
    #     # send file to host

