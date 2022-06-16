import socket

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('0.0.0.0', 59590))
        sock.listen(1)

        sock, address = sock.accept()
        print(f"{address} connected.")
        print(sock.recv(1024).decode('utf-8'))
        sock.sendall("world".encode('utf-8'))


if __name__ == '__main__':
    main()