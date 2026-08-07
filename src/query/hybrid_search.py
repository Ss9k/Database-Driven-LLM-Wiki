from src.utils.wiki_search import WikiSearch
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.vectorstore.faiss_store import faiss_store


class HybridSearch:

    def __init__(self):

        self.keyword_search = WikiSearch()

        self.embedding_generator = EmbeddingGenerator()

        self.vector_store = faiss_store

        self.reload()

    def reload(self):
        self.keyword_search = WikiSearch()
        self.embedding_generator.reload()
        self.vector_store.reload()
        self.vector_store.load()

    def search(self, query, top_k=5):
        

        keyword_results = self.keyword_search.retrieve_documents(
            query
        )

        query_embedding = self.embedding_generator.generate(
            query
        ).astype("float32")

        semantic_results = self.vector_store.search(
            query_embedding,
            top_k
        )
        
        merged = {}

        for doc in keyword_results:

            key = doc["path"]

            merged[key] = doc.copy()

            merged[key]["score"] = doc.get("score", 0)

        for doc in semantic_results:

            key = doc["path"]

            if key in merged:

                merged[key]["score"] += doc["score"]

            else:

                merged[key] = doc.copy()

        results = sorted(

            merged.values(),

            key=lambda x: x["score"],

            reverse=True

        )

        return results[:top_k]