import numpy as np
import json
import os
from .vector_store import VectorStore

class PersistentVectorStore(VectorStore):
    def __init__(self, storage_path="vector_db"):
        """Initialize a persistent vector store."""
        super().__init__()
        self.storage_path = storage_path
        self.metadata_path = os.path.join(storage_path, "metadata.json")
        self.vectors_path = os.path.join(storage_path, "vectors.npy")
        self._initialize_storage()
        self._load_if_exists()

    def _initialize_storage(self):
        """Create storage directory if it doesn't exist."""
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def _load_if_exists(self):
        """Load existing vectors and metadata if they exist."""
        if os.path.exists(self.metadata_path) and os.path.exists(self.vectors_path):
            # Load metadata
            with open(self.metadata_path, 'r') as f:
                metadata = json.load(f)
                self.vectors = {}
                # Load vectors
                all_vectors = np.load(self.vectors_path)
                for id, idx in metadata.items():
                    self.vectors[id] = all_vectors[idx]

    def save(self):
        """Save the current state to disk."""
        if not self.vectors:
            return

        # Convert vectors to a single numpy array
        vector_list = []
        metadata = {}
        for idx, (id, vector) in enumerate(self.vectors.items()):
            vector_list.append(vector)
            metadata[id] = idx

        # Save vectors
        vectors_array = np.array(vector_list)
        np.save(self.vectors_path, vectors_array)

        # Save metadata
        with open(self.metadata_path, 'w') as f:
            json.dump(metadata, f)

    def add(self, id, vector):
        """Override add to persist changes."""
        super().add(id, vector)
        self.save()

    def remove(self, id):
        """Override remove to persist changes."""
        result = super().remove(id)
        if result:
            self.save()
        return result

    def clear(self):
        """Clear all vectors and remove storage files."""
        super().__init__()  # Reset to empty state
        if os.path.exists(self.metadata_path):
            os.remove(self.metadata_path)
        if os.path.exists(self.vectors_path):
            os.remove(self.vectors_path) 