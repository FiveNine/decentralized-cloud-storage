import socket, pickle

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('0.0.0.0', 59590))
        sock.listen(1)

        sock_a, address_a = sock.accept()
        print(f"{address_a} connected.")

        sock_b, address_b = sock.accept()
        print(f"{address_b} connected.")

        sock_a.sendall(pickle.dumps(address_b))
        sock_b.sendall(pickle.dumps(address_a))
        print("Exchanged addresses, quitting now.")
        input()


if __name__ == '__main__':
    main()