# Filesystem

Kademlia filesystem implementation in python, will take it down
just need it up for distributed filesystems final project.

Kademlia is a DHT specification using XOR as a distance metric rather than
other things like how choord does it. Using xor has a lot of nice benefits,
and with the powers of hashing (or rather, hash functions behaving like oracles)
this can lead to well-distributed data.

### Implementation
- A global "filesystem" (where files cannot be deleted since it's easier that way)
    -  The filesystem is just a dictionary of dictionaries, with each "subdirectory"
       being a mapping of further subdirectories or files to their metadata
- A "file" is just a mapping of it's name to its metadata in this "filesystem" map
  where its metadata includes the hashes of all of it's chunks, in order
    - To recover the file, you ask nodes for all of its chunks and then reconstruct
      in order
- When you're adding a file to the "filesystem", you hash the file, chunk it up
  send the chunks to everyone (such that at least 20 people have it). The people
  you send it to should be the n closest nodes (where close is defined by the xor metric)
    - To find a file, you ask nodes closest to its chunks' hashes

- Periodically, a node will choose a random chunk from the filesystem and 
    query for it. If the number of responses is less than the ideal 20, it will
    request a "republish" which will essentially be a redistribution stage. The
    more nodes, the more often this happens obviously.
