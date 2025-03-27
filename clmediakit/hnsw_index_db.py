import hnswlib
import os
import threading
import numpy as np


class HNSWIndexDB:
    """
    A class to manage an HNSW index for storing and querying image/video hashes.
    """

    index_lock = threading.Lock()

    def __init__(self, index_path):
        """
        Initialize the HNSWIndexDB.

        Args:
            index_path (str): Path to store or load the HNSW index.
        """
        self.index_store = index_path
        index = hnswlib.Index(space="l2", dim=64)
        if os.path.exists(index_path):
            index.load_index(index_path, max_elements=200000)
            print(f"Loaded index from {index_path}")
        else:
            index.init_index(max_elements=200000, ef_construction=100, M=8)
            print("Initialized new index")
        self.index = index

    def add_hash(self, id, hash_bin_str: str):
        """
        Add a image/video hash to the index.

        Args:
            id (int): Unique identifier for the image/video.
            hash_val (list): Hash value of the image/video.
        """
        binary_str = str(hash_bin_str)[2:]  # e.g., "10110100..."
        binary_str = binary_str.ljust(64, "0")  # pad with zeros
        hash_val = np.array([float(bit) for bit in binary_str], dtype=np.float32)
        self.index.add_items([hash_val], [id])

    def add(self, id, hash_val):
        """
        Add a image/video hash to the index.

        Args:
            id (int): Unique identifier for the image/video.
            hash_val (list): Hash value of the image/video.
        """
        with HNSWIndexDB.index_lock:
            self.add_hash(id, hash_val)
            self.index.save_index(self.index_store)

    def replace(self, id, hash_val):
        """
        Replace a image/video hash in the index.

        Args:
            id (int): Unique identifier for the image/video.
            hash_val (list): Hash value of the image/video.
        """
        with HNSWIndexDB.index_lock:
            self.index.remove_items([id])
            self.add_hash(id, hash_val)
            self.index.save_index(self.index_store)

    def remove(self, id):
        """
        Remove a image/video hash from the index.

        Args:
            id (int): Unique identifier for the image/video.
        """
        with HNSWIndexDB.index_lock:
            self.index.remove_items([id])
            self.index.save_index(self.index_store)

    def query(self, hash_bin_str: str):
        """
        Query the index for similar image/video hashes.

        Args:
            hash_val (list): Hash value to query.

        Returns:
            tuple: A tuple containing IDs and distances of the nearest neighbors.
        """
        binary_str = str(hash_bin_str)[2:]  # e.g., "10110100..."
        binary_str = binary_str.ljust(64, "0")  # pad with zeros
        hash_val = np.array([float(bit) for bit in binary_str], dtype=np.float32)
        ids, distances = self.index.knn_query([hash_val], k=5)
        return ids, distances
