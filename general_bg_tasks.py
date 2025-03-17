import threading
import time

# every 1 second, probe a few nodes
# to see if their directories match
# if they don't, merge the trees together
VERIFY_DIRECTORY_INTERVAL = 1

# Rebalance our loads, i.e. redistribute the chunks we have
# if there are any closer/better nodes that should have them
REBALANCE_LOAD_INTERVAL = 10


def background_thread():
    last_verify_time = time.time()
    last_rebalance_time = time.time()
    while True:
        if time.time() - last_verify_time > VERIFY_DIRECTORY_INTERVAL:
            last_verify_time = time.time()
            # Verify the directory of the node
            # If it doesn't match, merge the trees together
            # TODO ^

        if time.time() - last_rebalance_time > REBALANCE_LOAD_INTERVAL:
            last_rebalance_time = time.time()
            # Rebalance the load on the nodes
            # TODO ^

        time.sleep(1)  # we don't need to do anything all that often
