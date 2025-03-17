# Import the xmlrpc library and do other
# stuff idk
import hashlib
import xmlrpc

from kademlia_dht import KNode, KTable, KBucket

us = KNode(hashlib.sha1("127.0.0.1:8000".encode()).hexdigest(), "127.0.0.1", 8000, 0)

# Initialize the DHT
dht = KTable(0)

# Add a node to the DHT
dht.add_node(1, "127.0.0.1", 8000)

# Main REPL
while True:
    pass
