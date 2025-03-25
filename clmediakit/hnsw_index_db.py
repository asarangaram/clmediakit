import hashlib
import os
import threading


class HNSWIndexDB:
    index_lock = threading.Lock()

    def __init__(self, index_path):
        self.index_store = index_path
        index = hashlib.Index(space="l2", dim=64)
        if os.path.exists(index_path):
            index.load_index(index_path, max_elements=200000)
            print(f"Loaded index from {index_path}")
        else:
            index.init_index(max_elements=200000, ef_construction=100, M=8)
            print("Initialized new index")
        self.index = index

    def add(self, video_id, hash_val):
        with HNSWIndexDB.index_lock:
            self.index.add_items([hash_val], [video_id])
            self.index.save_index(self.index_store)

    def query(self, hash_val):
        ids, distances = self.index.knn_query([hash_val], k=5)
        return ids, distances
