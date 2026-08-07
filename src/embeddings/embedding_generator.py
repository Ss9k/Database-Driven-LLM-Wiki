from sentence_transformers import SentenceTransformer
from pathlib import Path
from datetime import datetime
from src.database.metadata import metadata_db
from src.workspace.workspace import workspace
from src.utils.wiki_manager import (
    entities_path,
    concepts_path,
    summaries_path,
    topics_path
)

class EmbeddingGenerator:
    _shared_model = None

    def __init__(self):
        self.model = EmbeddingGenerator._shared_model
        # self.model = SentenceTransformer(
        #     "nomic-ai/nomic-embed-text-v1.5",
        #     trust_remote_code=True
        # )
        self.locations = {
            "entity": workspace.entities,
            "concept": workspace.concepts,
            "topic": workspace.topics,
            "summary": workspace.summaries,
        }

    def get_model(self):

        if EmbeddingGenerator._shared_model is None:

            print("Loading embedding model...")

            EmbeddingGenerator._shared_model = SentenceTransformer(
                "nomic-ai/nomic-embed-text-v1.5",
                trust_remote_code=True
            )

        self.model = EmbeddingGenerator._shared_model

        return self.model
    
    def generate(self, text: str):
        model = self.get_model()
        return model.encode(
            text,
            normalize_embeddings=True
        )
    

    
    def scan_wiki(self) -> list:

        pages = []

        for page_type, directory in self.locations.items():

            for file in directory.glob("*.md"):

                pages.append(
                    {
                        "title": file.stem,
                        "type": page_type,
                        "path": file,
                    }
                )

        return pages

    def generate_all_embeddings(self):

        results = []

        pages = self.scan_wiki()

        # ----------------------------
        # Sync metadata database
        # ----------------------------

        for page in pages:

            metadata_db.upsert_page(
                page["path"],
                page["title"],
                page["type"]
            )

        metadata_db.initialize_vector_ids()

        # ----------------------------
        # Generate embeddings
        # ----------------------------

        for page in pages:

            text = page["path"].read_text(
                encoding="utf-8"
            )

            embedding = self.generate(text)

            results.append(
                {
                    "title": page["title"],
                    "type": page["type"],
                    "path": str(page["path"]),
                    "vector_id": metadata_db.get_vector_id(
                        page["path"]
                    ),
                    "embedding": embedding,
                }
            )

        return results
    
    def get_modified_pages(self):

        modified = []

        pages = self.scan_wiki()

        for page in pages:

            current_modified = datetime.fromtimestamp(
                page["path"].stat().st_mtime
            ).isoformat()

            record = metadata_db.get_page(
                str(page["path"])
            )

            if record is None:

                modified.append(page)

                continue

            stored_modified = record[3]

            if current_modified != stored_modified:

                modified.append(page)

        return modified

    def generate_modified_embeddings(self):

        results = []

        modified_pages = self.get_modified_pages()

        for page in modified_pages:

            text = page["path"].read_text(
                encoding="utf-8"
            )

            embedding = self.generate(text)

            metadata_db.upsert_page(
                page["path"],
                page["title"],
                page["type"]
            )

            results.append(
                {
                    "title": page["title"],
                    "type": page["type"],
                    "path": str(page["path"]),
                    "embedding": embedding,
                }
            )

        return results
    
    def reload(self):

        self.locations = {
            "entity": workspace.entities,
            "concept": workspace.concepts,
            "topic": workspace.topics,
            "summary": workspace.summaries,
        }