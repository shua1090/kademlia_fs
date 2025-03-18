# Import the xmlrpc library and do other
# stuff idk
import hashlib
import xmlrpc

import dht
from kademlia_dht import KNode, KTable, KBucket

port_temp = input("port? ")
us = KNode(
    hashlib.sha1(f"localhost:{port_temp}".encode()).hexdigest(),
    "localhost",
    int(port_temp),
    0,
)

our_dht_handler = dht.DHT(us)

# Main REPL
while True:
    command = input("> ")
    if command == "exit":
        break
    elif command == "start":
        our_dht_handler.start_server("localhost", int(port_temp))
    elif command == "add":
        input_file = input("File: ")
        path = input("Path in DHT: ")
        our_dht_handler.add_file(input_file, path)
    elif command == "get":
        path = input("Path in DHT: ")
        our_dht_handler.get_file(path)
    elif command == "list":
        our_dht_handler.list_files()

    # Show the ktable
    elif command == "nodes":
        print(our_dht_handler.table)
