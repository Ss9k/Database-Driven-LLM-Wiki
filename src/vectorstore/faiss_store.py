import faiss
import numpy as np
from pathlib import Path
import pickle
from src.workspace.workspace import workspace

class FAISSStore:

    def __init__(self, dimension: int = 768):

        self.dimension = dimension

        self.index = faiss.IndexIDMap2(
            faiss.IndexFlatIP(768)
        )
        self.storage_path = workspace.faiss

        self.storage_path.mkdir(
            parents=True,
            exist_ok=True
            )
        

        self.index_path = self.storage_path / "index.faiss"

        self.metadata_path = self.storage_path / "metadata.pkl"
        self.metadata = {}
        self.reload()

    def add_embeddings(self, pages):

        vectors = []
        ids = []

        for page in pages:

            vectors.append(
                page["embedding"]
            )

            ids.append(
            page["vector_id"]
            
            )
            self.metadata[page["vector_id"]] = {
                "vector_id": page["vector_id"],
                "title": page["title"],
                "type": page["type"],
                "path": page["path"],
            }

        vectors = np.array(
            vectors,
            dtype="float32"
        )
        ids = np.array(ids,dtype="int64")

        self.index.add_with_ids(vectors, ids)

    def size(self):

        return self.index.ntotal
    
    def save(self):

        faiss.write_index(
            self.index,
            str(self.index_path)
        )

        with open(
            self.metadata_path,
            "wb"
        ) as f:

            pickle.dump(
                self.metadata,
                f
            )
    
    def load(self):

        if self.index_path.exists():

            self.index = faiss.read_index(
                str(self.index_path)
            )

        if self.metadata_path.exists():

            with open(
                self.metadata_path,
                "rb"
            ) as f:

                self.metadata = pickle.load(f)

    def search(self, query_embedding, top_k=5):

        import numpy as np

        query_embedding = np.array(
            [query_embedding],
            dtype="float32"
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            page = self.metadata[int(idx)].copy()

            page["score"] = float(score)

            results.append(page)

        return results
    
    def rebuild_from_embeddings(self, embeddings):

        self.index = faiss.IndexIDMap2(
            faiss.IndexFlatIP(768)
        )

        self.metadata = {}

        vectors = []
        ids = []

        for item in embeddings:

            vectors.append(
                item["embedding"]
            )

            ids.append(
                item["vector_id"]
            )

            self.metadata[item["vector_id"]] = {
                "vector_id": item["vector_id"],
                "title": item["title"],
                "type": item["type"],
                "path": item["path"],
            }

        if vectors:

            vectors = np.array(
                vectors,
                dtype=np.float32
            )

            ids = np.array(
                ids,
                dtype=np.int64
            )

            self.index.add_with_ids(
                vectors,
                ids
            )

        self.save()

    def remove_page(self, vector_id):

        ids = np.array(
            [vector_id],
            dtype=np.int64
        )

        self.index.remove_ids(ids)

        if vector_id in self.metadata:
            del self.metadata[vector_id]


    def update_page(self, page):

        vector_id = page["vector_id"]

        # Remove old vector
        self.remove_page(vector_id)

        # Add updated vector
        vector = np.array(
            [page["embedding"]],
            dtype=np.float32
        )

        ids = np.array(
            [vector_id],
            dtype=np.int64
        )

        self.index.add_with_ids(
            vector,
            ids
        )

        # Update metadata
        self.metadata[vector_id] = {
            "vector_id": vector_id,
            "title": page["title"],
            "type": page["type"],
            "path": page["path"],
        }

        self.save()

    def reload(self):

        self.storage_path = workspace.faiss

        self.storage_path.mkdir(
            parents=True,
            exist_ok=True
        )

        self.index_path = self.storage_path / "index.faiss"

        self.metadata_path = self.storage_path / "metadata.pkl"
        self.index = faiss.IndexIDMap2(
        faiss.IndexFlatIP(self.dimension)
    )
        self.metadata = {}
        self.load()

faiss_store = FAISSStore()