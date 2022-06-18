import Utilities.utility_methods as utils
import socket, threading
from queue import Queue
from typing import TypeVar
Any = TypeVar('Any')

class RelayServer:

    def __init__(self) -> socket.socket:
        self.queue_of_hosts: Queue[tuple[socket.socket, tuple[str, int]]] = Queue()
        
        self.main_threads: list[threading.Thread] = []
        self.accept_threads: list[threading.Thread] = []

        self.STOP_ACCEPTING_CONNECTIONS = threading.Event()
        self.STOP_ACCEPTING_CONNECTIONS.clear()

    def __accept_connections(self):
        print(f"Accepting connections on port 59590.")
        connected_sockets: list[socket.socket] = []
        while not self.STOP_ACCEPTING_CONNECTIONS.is_set():
            # print(f"Connected sockets: {len(connected_sockets)}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('0.0.0.0', 59590))
            sock.listen(5)

            sock.settimeout(3)
            try:
                sock, address = sock.accept()
            except Exception as e:
                print(e)
                continue
            else:
                sock.settimeout(None)
                print(f"Connection established with {address}.")
                accept_thread = threading.Thread(target=self.__handle_client, args=(sock, address,))
                accept_thread.start()
                self.accept_threads.append(accept_thread)
                connected_sockets.append(sock)

        if self.STOP_ACCEPTING_CONNECTIONS.is_set():
            for sock in connected_sockets:
                sock.close()

    def __handle_client(self, sock: socket.socket, address: tuple[str, int]) -> None:
        choice = self.receive_message(sock)
        print(f"Client chose {choice}")
        print()
        if choice == "Host":
            print(f"Host {address} added to list of hosts.")
            self.queue_of_hosts.put((sock, address))

        elif choice == "Client":
            print(f"Client {address} requires a host.")
            # wait for a host to be available
            while self.queue_of_hosts.qsize() == 0:
                pass
            # exchange addresses
            host_sock, host_address = self.queue_of_hosts.get()
            address = utils.address_to_string(address)
            host_address = utils.address_to_string(host_address)
            self.send_message(host_sock, address)
            print(f"Host {host_address} has received client {address}.")
            self.send_message(sock, host_address)
            print(f"Client {address} has received host {host_address}.")
        
    def start_server(self):
        print(25*"=" + "Server has started!" + 25*"=")
        
        listen_thread = threading.Thread(target=self.__accept_connections)
        listen_thread.start()
        self.main_threads.append(listen_thread)

    def stop_server(self):
        self.STOP_ACCEPTING_CONNECTIONS.set()
        print(25*"=" + "Server has stopped." + 25*"=")
        

    def send_message(self, sock: socket.socket, message: str) -> None:
        raw_data = message.encode('utf-8')
        data_length = len(raw_data).to_bytes(4, byteorder='big')

        sock.sendall(data_length)
        sock.sendall(raw_data)

    def receive_message(self, sock: socket.socket) -> str:
        data_length = sock.recv(4)
        data_length = int.from_bytes(data_length, byteorder='big')

        # receive message with a buffer of 4KB
        message = bytearray(data_length)
        received_bytes = 0
        while received_bytes < data_length:
            remaining = data_length - received_bytes
            message.extend(sock.recv(remaining if remaining < 4096 else 4096))
            received_bytes = len(message)

        return message.decode('utf-8')
