# A filesystem in our implementation
# is a global "directory tree"
# that maps directory names to file metadata
# and file metadata to file chunks
import hashlib
import os
import pathlib


class FileSystem:
    def __init__(self):
        # Reference file_metadata in file_utils.py
        self.root: dict[str, any] = {}

    def _traverse_to_directory(
        self, path: str, create_if_missing: bool = False
    ) -> dict:
        """Traverse the directory tree to reach the specified path.

        Args:
            path (str): The path to traverse to
            create_if_missing (bool, optional): Whether to create directories if they don't exist. Defaults to False.

        Returns:
            dict: The directory at the specified path

        Raises:
            FileNotFoundError: If the path doesn't exist and create_if_missing is False
        """
        path_parts = pathlib.Path(path).parts
        current_dir = self.root

        for part in path_parts:
            if part not in current_dir:
                if create_if_missing:
                    current_dir[part] = {}
                else:
                    raise FileNotFoundError(f"Directory {part} not found")
            current_dir = current_dir[part]

        return current_dir

    def add_file_to_directory(self, directory_name, file_name, file_metadata):
        """Add a file to a directory

        Args:
            directory_name (str): The name of the directory to add the file to
            file_name (str): The name of the file to add
            file_metadata (dict): The metadata of the file
        """
        current_dir = self._traverse_to_directory(
            directory_name, create_if_missing=True
        )
        current_dir[file_name] = file_metadata

    def make_dirs(self, directory_name):
        """Make a directory in the filesystem
            it's like mkdir -p

        Args:
            directory_name (_type_): _description_
        """
        self._traverse_to_directory(directory_name, create_if_missing=True)

    def get_file(self, file_name):
        # Split path into parts and get the directory containing the file
        path_parts = pathlib.Path(file_name).parts
        directory_path = str(
            pathlib.Path(*path_parts[:-1]) if len(path_parts) > 1 else ""
        )
        current_dir = self._traverse_to_directory(directory_path)

        # Get the file from the final directory
        if path_parts[-1] not in current_dir:
            raise FileNotFoundError(f"File {path_parts[-1]} not found")

        return current_dir[path_parts[-1]]

    def generate_merkle_tree(self, path: str):
        # Generate a merkle tree for the filesystem
        # This computes the "hash" of the current filesystem
        # by recursively hashing the contents of each directory

        # Get the contents of the directory
        directory_contents = self._traverse_to_directory(path)
        print("contents", directory_contents.keys())

        # Hash the contents of the directory
        directory_hash = [
            (
                directory_contents[subpath]["file_hash"]
                if directory_contents[subpath].get("is_file", False)
                else self.generate_merkle_tree(
                    os.path.join(path, subpath) if path else subpath
                )
            )
            for subpath in directory_contents.keys()
        ]

        # Typically you would hash the directory contents, but
        # we'll just xor it all together since order doesn't matter
        # and all that yada yada
        xor_hash = 0
        for hash in directory_hash:
            xor_hash ^= hash

        return xor_hash

    def __repr__(self):
        def format_dir(directory, indent=0):
            result = []
            for name, contents in directory.items():
                if isinstance(contents, dict):
                    # This is a directory (don't add the / if it's the root)
                    if indent == 0:
                        result.append(" " * indent + name)
                    else:
                        result.append(" " * indent + name + "/")
                    result.extend(format_dir(contents, indent + 2))
                else:
                    # This is a file
                    result.append(" " * indent + name)
            return result

        return "\n".join(format_dir(self.root))


if __name__ == "__main__":
    fs = FileSystem()
    fs.make_dirs("/test/test2/test3")
    # Just messing around with the file hash
    fs.add_file_to_directory(
        "/test/test2/test3",
        "test.txt",
        {"is_file": True, "file_hash": int(hashlib.sha1(b"test.txt").hexdigest(), 16)},
    )
    fs.add_file_to_directory(
        "/",
        "test2.txt",
        {
            "is_file": True,
            "file_hash": int(hashlib.sha1(b"test2.txt").hexdigest(), 16),
        },
    )
    print(fs)
    print(fs.generate_merkle_tree("/"))
