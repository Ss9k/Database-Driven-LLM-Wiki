import numpy as np

from src.embeddings.embedding_generator import EmbeddingGenerator


class DuplicateDetector:

    def __init__(self):

        self.embedding_generator = EmbeddingGenerator()

    def detect(self, threshold=0.92):

        self.embedding_generator.reload()

        pages = self.embedding_generator.generate_all_embeddings()

        duplicates = []

        for i in range(len(pages)):
            for j in range(i + 1, len(pages)):
                a = pages[i]
                b = pages[j]
                if (
                a["title"] == b["title"]
                and
                a["type"] != b["type"]):
                    continue

                similarity = float(
                    np.dot(
                        a["embedding"],
                        b["embedding"]
                    )
                )

                if similarity >= threshold:

                    duplicates.append(
                        {
                            "page1": a["title"],
                            "page2": b["title"],
                            "score": round(similarity, 3),
                        }
                    )

        return duplicates