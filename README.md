# Decentralized Cloud Storage
## Prerequisites
-   Python 3.10.0+
-   [Pickle](https://pypi.org/project/pickle5/)
```
pip install pickle
```

## How To Run
1.  Clone this repository:
```
git clone https://github.com/FiveNine/decentralized-cloud-storage.git
```
2.  Transfer these files to a relay server with a static public IPv4 address.
    - [run_relay_server.py](/Server/run_relay_server.py)
    - [tcp_relay_server.py](/Server/tcp_relay_server.py)
    - [udp_server.py](/Server/udp_server.py)
3.  Transfer these files to the peers. Peers can be behind different NATs as long as they dont use Symmetric NAT.
    - [run_client_as_customer.py](/Client/run_client_as_customer.py)
    - [run_client_as_host.py](/Client/run_client_as_host.py)
    - [tcp_client.py](/Client/tcp_client.py)
    - [udp_client.py](/Client/udp_client.py)
4.  In [run_client_as_customer.py](/Client/run_client_as_customer.py) and [run_client_as_host.py](/Client/run_client_as_host.py) set server address to be the relay server's public IPv4 address.
5.  Run [run_relay_server.py](/Server/run_relay_server.py) on the **Relay Server**.
6.  Run [run_client_as_customer.py](/Client/run_client_as_customer.py) on one peer and [run_client_as_host.py](/Client/run_client_as_host.py) on another peer.
