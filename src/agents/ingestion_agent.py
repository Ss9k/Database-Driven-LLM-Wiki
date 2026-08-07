from pathlib import Path

from src.agents.extraction_agent import ExtractionAgent

from src.utils.wiki_manager import (
    create_or_update_summary_page,
    create_or_update_entity_page,
    create_or_update_concept_page,
    create_or_update_topic_page,
    update_index,
    log_activity,
)
from workflows import state


class IngestionAgent:

    def __init__(self):

        self.extractor = ExtractionAgent()

    def ingest_document(self, source_path):

        source_path = Path(source_path)

        text = source_path.read_text(
            encoding="utf-8"
        )

        knowledge = self.extractor.extract(text)

        summary = knowledge["summary"]

        entities = knowledge["entities"]

        concepts = knowledge["concepts"]

        document_name = source_path.stem

        create_or_update_summary_page(
            document_name,
            summary
        )

        for entity in entities:

            create_or_update_entity_page(
                entity["name"],
                entity["summary"],
                state["document_name"]
            )

        for concept in concepts:

            create_or_update_concept_page(
                concept["name"],
                concept["definition"],
                state["document_name"]
            )

        log_activity(
            f"Ingested source: {document_name}"
        )

        return knowledge