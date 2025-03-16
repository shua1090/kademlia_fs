### file_utils.py

from datetime import datetime
import os
import hashlib

CHUNK_SIZE = 1024 * 256  # 256 kB data


def split_and_hash_file(file_path):
    """Split a file into chunks and hash each chunk

    Args:
        file_path (str): The path to the file to split
    """

    # Read the file
    with open(file_path, "rb") as f:
        data = f.read()

    # Split the file into chunks
    chunks = [data[i : i + CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]
    # Hash each chunk (this is the key to the chunk)
    hashes = [hashlib.sha1(chunk).hexdigest() for chunk in chunks]

    # File_path to name:
    file_name = os.path.basename(file_path)

    file_metadata = {
        # Name of the file
        "file_name": file_name,
        # Reference to the "whole file"
        "file_hash": hashlib.sha1(data).hexdigest(),
        # Hashes of the chunks, which are required to reconstruct the file
        "hashes": hashes,
        # Date added
        "date_added": datetime.now().isoformat(),
    }

    return file_metadata, chunks


def regenerate_file(file_metadata, chunks):
    """Load a file from the chunks and hashes

    Args:
        file_metadata (dict): The metadata of the file
        chunks (list): The chunks of the file
    """

    ordered_chunks = []

    for hash in file_metadata["hashes"]:
        # Find the chunk with the correct hash
        for chunk in chunks:
            if hashlib.sha1(chunk).hexdigest() == hash:
                ordered_chunks.append(chunk)
                break  # break from the for chunk in chunks loop

    # Reconstruct the file from the ordered chunks
    file_data = b"".join(ordered_chunks)
    return file_data
