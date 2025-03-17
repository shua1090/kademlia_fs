# Node adding themselves to the network
Node calls <add_node> to one of the nodes
already in the network to get added.

If a node already has this new node, it doesn't forward the message
else it calls add_node for all of its nodes, thus telling everyone
about this new node!

# Node adding a file to the filesystem
Node splits up the file and all that, then sends the chunk to the
20 closest nodes to the chunk's hash by searching the KBucket for that distance
etc. These nodes will take in this chunk if they don't already have it. "add_chunk"

Once the file has been added, the node calls add_file(path) to add the file
to the directory tree. This directory tree change is forwarded to all nodes, all
of whom verify consistency with a merkle tree hash. How does this work?
When you create a new file or directory, you call "merge_tree" with another node's
directory tree, which merges it all up. idk.

Periodically, nodes will choose a random chunk from the directory tree and
query its existence. If it gets less than 10 responses, it will request
the republishing of the chunk (which is the same function call as "add_chunk")
