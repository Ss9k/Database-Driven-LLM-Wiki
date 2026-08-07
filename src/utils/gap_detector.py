from pathlib import Path

from src.utils.wiki_manager import (
    entities_path,
    concepts_path,
    create_stub_page,
    log_activity
)


class GapDetector:

    def __init__(self):
        pass

    def detect(self, entities, concepts, source_name):

        missing_entities = []
        missing_concepts = []

        for entity in entities:

            entity_file = entities_path()/ f"{entity}.md"

            if not entity_file.exists():

                create_stub_page(
                    entity,
                    source_name
                )

                missing_entities.append(entity)

        for concept in concepts:

            concept_file = concepts_path()/ f"{concept}.md"

            if not concept_file.exists():

                missing_concepts.append(concept)

        if missing_entities:

            log_activity(
                f"Gap detected (entities): {', '.join(missing_entities)}"
            )

        if missing_concepts:

            log_activity(
                f"Gap detected (concepts): {', '.join(missing_concepts)}"
            )

        return {

            "entities": missing_entities,

            "concepts": missing_concepts

        }