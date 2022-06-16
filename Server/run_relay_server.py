from tcp_relay_server import RelayServer

server = RelayServer()
server.start_server()

if input("Type \"stop\" to stop server\n") == "stop":
    server.stop_server()