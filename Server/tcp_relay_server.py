import socket, pickle, threading
from queue import Queue
from typing import TypeVar
T = TypeVar('T')

class RelayServer:

    def __init__(self) -> socket.socket:
        self.queue_of_hosts = Queue()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock.bind(('0.0.0.0', 59590))

        self.STOP_ACCEPTING_CONNECTIONS = threading.Event()
        self.STOP_ACCEPTING_CONNECTIONS.clear()

    def __accept(self) -> None:
        print(f"Accepting connections on port 59590.")
        while not self.STOP_ACCEPTING_CONNECTIONS.is_set():
            self.sock.settimeout(5)
            try:
                self.sock, address = self.sock.accept()
            except socket.timeout:
                continue
            self.sock.settimeout(None)

            print(f"Connection established with {address}.")

            choice = self.receive_message()
            if choice == "Host":
                print(f"Host {address} added to list of hosts.")
                self.queue_of_hosts.put(address)
            elif choice == "Client":
                print(f"Client {address} requires a host.")
                self.send_message(self.queue_of_hosts.get())

    def start_server(self):
        self.sock.listen(5)
        print(25*"=" + "Server has started!" + 25*"=")
        accept_thread = threading.Thread(target=self.__accept)
        accept_thread.start()
        
    def stop_server(self):
        self.STOP_ACCEPTING_CONNECTIONS.set()
        self.sock.close()

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
