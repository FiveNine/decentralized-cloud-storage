from tcp_client import Client

server_address = ('51.142.79.26', 59590)

choice = input("Default port is 59590.\nDo you wish to use a custom TCP port? (y/n)\n")

if choice == 'y':
    while True:
        try:
            port = int(input("Enter an open TCP port you wish to use:\n"))
        except:
            print("Invalid input.")
            continue
        else:
            break
elif choice == 'n':
    port = 59590

client = Client(server_address, port)
client.join_queue()

print(client.receive_message())
client.send_message("Hello Client! I got your files!")