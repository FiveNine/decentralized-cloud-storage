from tcp_client import Client

server_address = ('51.142.79.26', 59590)

client = Client(server_address)
client.join_queue()

print(client.receive_message())