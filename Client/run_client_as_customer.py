from tcp_client import Client

server_address = ('', 59590)

client = Client(server_address)
client.find_host()

client.send_message("Hello World!")