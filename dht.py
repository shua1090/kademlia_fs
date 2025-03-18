import xmlrpc.client
from kademlia_dht import KNode, KTable
import xmlrpc.server
import threading
import time
from filesystem_impl import FileSystem


class DHT:
    def __init__(self, our_node: KNode):
        self.n = 20
        self.table: KTable = KTable(our_node.id)
        self.server = None
        self.server_thread = None
        self.our_node = our_node

        self.directory_tree = FileSystem()

    def start_server(self, host: str, port: int):
        """Start the XML-RPC server to expose DHT methods.

        Args:
            host (str): The host address to bind to
            port (int): The port to listen on
        """

        class DHTRPCServer(xmlrpc.server.SimpleXMLRPCServer):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs, logRequests=False)
                self.register_introspection_functions()

        self.server = DHTRPCServer((host, port))
        self.server.register_instance(self)

        # Start server in a separate thread
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

        def add_ourselves_to_others(self):
            """Add ourselves to the DHT table of other nodes every 1s."""
            while True:
                for i in range(10):
                    if 8000 + i != self.our_node.port:
                        try:
                            # print("adding ourselves to port", 8000 + i)
                            # Call add_node on localhost:8000 + i
                            xmlrpc.client.ServerProxy(
                                f"http://localhost:{8000 + i}"
                            ).add_node(self.our_node.id, "localhost", 8000 + i)
                        except ConnectionRefusedError as e:
                            # This is fine, the node is not running
                            pass
                time.sleep(1)

        def sync_directory_tree(self):
            """Periodically sync the directory tree with the DHT table."""

            while True:
                for node in self.table.get_all_nodes():
                    # Verify that the top level hashes are the same
                    # Dial the node and get the top level hash
                    proxy = xmlrpc.client.ServerProxy(f"http://{node.ip}:{node.port}")
                    top_level_hash = proxy.get_top_level_hash()
                    if top_level_hash != self.get_top_level_hash():
                        # Unequal directory trees, merge the trees
                        # Download the directory tree from the node
                        self.merge_directory_tree(proxy.get_directory_tree())
                        proxy.merge_directory_tree(self.get_directory_tree())
                time.sleep(1)

        threading.Thread(target=add_ourselves_to_others, args=(self,)).start()
        threading.Thread(target=sync_directory_tree, args=(self,)).start()

    def merge_directory_tree(self, directory_tree: FileSystem):
        """Merge a directory tree into the current directory tree."""
        self.directory_tree.merge(directory_tree)

    def get_top_level_hash(self):
        """Get the top level hash of the directory tree."""
        return self.directory_tree.generate_merkle_tree("/")

    def stop_server(self):
        """Stop the XML-RPC server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            if self.server_thread:
                self.server_thread.join()

    def add_node(self, node_id: int, ip: str, port: int) -> bool:
        """Add a node to the DHT table.

        Args:
            node_id (int): The unique identifier of the node
            ip (str): The IP address of the node
            port (int): The port number of the node

        Returns:
            bool: True if the node was added successfully
        """
        try:
            self.table.add_node(node_id, ip, port)
            return True
        except Exception as e:
            print(f"Error adding node: {e}")
            return False

    def merge_directory_tree(self, directory_tree: FileSystem):
        """Merge a directory tree into the current directory tree."""
        self.directory_tree.merge(directory_tree)

    def add_file(self, file_path, path_in_dht):
        # TODO
        pass

    def add_chunk(self, file_path, path_in_dht):
        # TODO
        pass

    def get_file(self, path_in_dht):
        # TODO
        pass

    def list_files(self):
        # TODO
        pass
