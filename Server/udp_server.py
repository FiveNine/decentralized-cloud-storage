import socket
import pickle
import random
import threading

server_address = ("0.0.0.0", 59420)

print(30 * "-" + "\n\tServer Started\n" + "-" * 30)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind(("0.0.0.0", 59420))

    # Accept message from both clients to get their addresses
    msg, address_a = sock.recvfrom(1024)
    print(f"Connection Accepted from: {address_a} : {msg}")

    msg, address_b = sock.recvfrom(1024)
    print(f"Connection Accepted from: {address_b} : {msg}")

    # Exchange client addresses
    sock.sendto(pickle.dumps((address_b[0], address_b[1], True)), address_a)
    sock.sendto(pickle.dumps((address_a[0], address_a[1], False)), address_b)

    # msg, address = sock.recvfrom(1024)
    # print(msg.decode("utf-8"))
    # print(address, address_a, address_b)


# class Server:
#     def __init__(self, ip, port):
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.socket.bind((ip, port))

#     def accept_connections(self):
#         thread = threading.Thread(target=self.ThreadFunctionality)
#         thread.start()
#         msg, address_a = self.socket.recvfrom(1)
#         msg, address_b = self.socket.recvfrom(1)
