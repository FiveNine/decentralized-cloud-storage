import socket, pickle

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('0.0.0.0', 59590))
        sock.listen(1)

        while True:
            print("Waiting for first connection...")
            sock.settimeout(3)
            try:
                sock_a, address_a = sock.accept()
            except socket.timeout:
                continue
            else:
                print(f"{address_a} connected.")
                sock.settimeout(None)
                break

        while True:
            print("Waiting for second connection...")
            sock.settimeout(3)
            try:
                sock_b, address_b = sock.accept()
            except socket.timeout:
                continue
            else:
                print(f"{address_b} connected.")
                sock.settimeout(None)
                break

        sock_a.sendall(pickle.dumps(address_b))
        sock_b.sendall(pickle.dumps(address_a))
        print("Exchanged addresses, quitting now.")
        input()


if __name__ == '__main__':
    main()