import socket
import pickle
import time

# import utils
from typing import Tuple

server_address = ("51.142.79.26", 59590)

print(10 * "-" + "Client started!" + "-" * 10)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    # Give server my address
    sock.sendto(b"\xff", server_address)
    print("Connected to server")

    # Receive other client's address from server
    msg, address = sock.recvfrom(1024)
    msg = pickle.loads(msg)
    print(f"Message from {address} : {msg}")

    # process the message sent from server,
    # message is sent in format: (ip, port, bool)
    # bool specifies whether this client should
    # receive message or send message from/to other client
    become_server = msg[2]
    other_address = (msg[0], msg[1])

    # initially, both clients message each other
    # to punch the hole through NAT
    sock.sendto(b"\xff", other_address)
    sock.recvfrom(1)

    if become_server:
        msg, address = sock.recvfrom(1024)
        print(f"Message from {address} : {msg.decode('ascii')}")

    else:
        sock.sendto("Found you!".encode("ascii"), other_address)
        print(f"Sent message to {other_address}")


# class Client:
#     def __init__(self, isHost):
#         self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.isHost = isHost
#         self.hostList = []

#     def ConnectToServer(self, serverAddress: Tuple[str, int]):
#         self.sock.settimeout(10)
#         print("Attempting to connect to server.")
#         utils.SendMessage(self.sock,)
#         address = ''
#         while address != serverAddress:
#             try:
#                 self.sock.sendto(pickle.dumps(self.isHost), serverAddress)
#                 receivedClients, address = sock.recvfrom(1024)
#                 self.hostList = pickle.loads(receivedClients)
#             except:
#                 print("Connection failed, Retrying in 10 seconds...")
#                 time.sleep(10)
