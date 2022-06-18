import socket, time
import Utilities.utils as utils

from typing import TypeVar
Any = TypeVar('Any')

class Client:
    def __init__(self, server_address : tuple[str, int], port: int) -> socket.socket:
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock.bind(('0.0.0.0', self.port))

        self.relay_server_address = server_address

    # not being used
    def __accept(self) -> None:
        print(f"Accepting connection on port 59590.")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
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
                self.sock = connection

    def __connect(self, address: tuple[str, int]) -> None:
        print(f"Connecting from {('0.0.0.0', self.port)} to {address}.")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sock.bind(('0.0.0.0', self.port))

        while True:
            try:
                sock.settimeout(3)
                sock.connect(address)
            except (socket.error, socket.timeout) as e:
                print(e)
                if e == socket.error:
                    time.sleep(3)
                continue
            else:
                print("Connection Established!")
                sock.settimeout(None)
                return sock
    
    def join_queue(self) -> None:
        self.sock = self.__connect(self.relay_server_address)
        self.send_message("Host")

        # wait until relay server finds a client
        other_address = self.receive_message()
        other_address = utils.string_to_address(other_address)

        print(f"Server sent client: {other_address}")
        self.sock = self.__connect(other_address)

        print("Will now receive message from other client.")
    
    def find_host(self) -> None:
        self.sock = self.__connect(self.relay_server_address)
        self.send_message("Client")

        # relay server finds appropriate host and sends address
        other_address = self.receive_message(self.sock)
        other_address = utils.string_to_address(other_address)

        print(f"Server sent client: {other_address}")
        self.sock = self.__connect(other_address)

        print("Will now send message to other client.")

    def send_message(self, message: str) -> None:
        raw_data = message.encode('utf-8')
        data_length = len(raw_data).to_bytes(4, byteorder='big')

        self.sock.sendall(data_length)
        self.sock.sendall(raw_data)

    def receive_message(self) -> str:
        data_length = self.sock.recv(4)
        data_length = int.from_bytes(data_length, byteorder='big')

        # receive message with a buffer of 4KB
        message = bytearray(data_length)
        received_bytes = 0
        while received_bytes < data_length:
            remaining = data_length - received_bytes
            message.extend(self.sock.recv(remaining if remaining < 4096 else 4096))
            received_bytes = len(message)

        return message.decode('utf-8')

    # def send_file(self, file_path: str) -> None:
    #     # send file to host

