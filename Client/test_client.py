import socket, sys

def addr_from_args(args):
    if(args[2] == 'receive'):
        return int(args[1]), True
    return int(args[1]), False

def main(port=59590, receive = False):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        other_port = 59590
        if port == 59590:
            other_port = 59591
        sock.bind(('127.0.0.1', port))
        sock.connect(('127.0.0.1', other_port))

        if receive:
            print(sock.recv(1024).decode('ascii'))
        else:
            sock.send('Hello'.encode('ascii'))
            print("Sent message")


if __name__ == '__main__':
    main(*addr_from_args(sys.argv))