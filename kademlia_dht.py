### Kademlia.py

import hashlib
import math
import random
import time

MAX_LAST_SEEN = 10


def string_hex_id_to_int(hex_id):
    return int(hex_id, 16)


class KNode:
    def __init__(self, id: str, ip, port, last_seen):
        self.id = id
        self.ip = ip
        self.port = port
        self.last_seen = last_seen

    def seen_again(self):
        self.last_seen = time.time()

    def get_distance(self, id: str):
        return string_hex_id_to_int(id) ^ string_hex_id_to_int(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"KNode(id={self.id}, ip={self.ip}, port={self.port}, last_seen={self.last_seen})"


class KTable:
    def __init__(self, our_id: str):
        self.our_id = our_id
        self.buckets = [KBucket(2**i, 2 ** (i + 1), 20) for i in range(160)]

    def get_all_nodes(self):
        for bucket in self.buckets:
            for node in bucket.nodes:
                yield node

    def get_bucket(self, distance):
        """Get the bucket for a given distance

        Args:
            distance (int): The distance to the target node

        Returns:
            KBucket: The bucket for the given distance

        Returns:
            _type_: _description_
        """
        return self.buckets[int(math.log(distance, 2))]

    def add_node(self, node_id, ip, port):
        """Add a node to the table, if it's not already there

        Args:
            node_id (int): The ID of the node to add
            ip (str): The IP address of the node
            port (int): The port of the node
        """
        # Add to the bucket with the correct distance
        bucket = self.get_bucket(
            string_hex_id_to_int(node_id) ^ string_hex_id_to_int(self.our_id)
        )
        bucket.add_node(KNode(node_id, ip, port, time.time()))

    def find_closest_nodes(self, target_id: str, count=20):
        bucket = self.get_bucket(
            string_hex_id_to_int(target_id) ^ string_hex_id_to_int(self.our_id)
        )
        return bucket.find_closest_nodes(target_id, count)

    def __repr__(self):
        return "\n".join(
            filter(
                lambda x: x != "",
                [
                    (
                        f"KBucket(min_id={bucket.min_id}, max_id={bucket.max_id}, nodes={bucket.nodes})"
                        if bucket.nodes
                        else ""
                    )
                    for bucket in self.buckets
                ],
            )
        )


class KBucket:
    def __init__(self, min_id, max_id, max_nodes):
        self.min_id = min_id
        self.max_id = max_id
        self.nodes = []
        self.max_nodes = max_nodes

    def get_distance(self, id: str):
        """Get the distance between the node and the min ID

        Args:
            id (int): The ID of the node

        Returns:
            int: The distance between the node and the min ID
        """
        return string_hex_id_to_int(id) ^ self.min_id

    def add_node(self, node):
        """Add a node to the bucket, if it's not already in the bucket

        Args:
            node (KNode): The node to add
        """
        # If the node is not already in the bucket, add it
        if node.id not in [node.id for node in self.nodes]:
            if len(self.nodes) < self.max_nodes:
                self.nodes.append(node)
            else:
                # Remove nodes that haven't been seen in MAX_LAST_SEEN seconds
                self.nodes = [
                    node
                    for node in self.nodes
                    if time.time() - node.last_seen < MAX_LAST_SEEN
                ]
                if len(self.nodes) < self.max_nodes:
                    self.nodes.append(node)
                else:
                    # Remove the furthest node if it's further than the new node
                    furthest_node = max(
                        self.nodes, key=lambda x: x.get_distance(self.min_id)
                    )
                    if furthest_node.get_distance(self.min_id) > node.get_distance(
                        self.min_id
                    ):
                        self.nodes.remove(furthest_node)
                        self.nodes.append(node)

        else:
            # Update the last seen time of the node
            self.nodes[self.nodes.index(node)].last_seen = time.time()

    def __len__(self):
        return len(self.nodes)

    def __repr__(self):
        return (
            f"KBucket(min_id={self.min_id}, max_id={self.max_id}, nodes={self.nodes})"
        )
