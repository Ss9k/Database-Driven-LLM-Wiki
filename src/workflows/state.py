from typing import TypedDict


class WikiState(TypedDict):

    # Input
    source_path: str

    # Source Information
    source_text: str
    document_name: str

    # LLM Extraction
    summary: str
    entities: list[str]
    concepts: list[str]
    claims: list[str]

    # Contradiction Detection
    contradictions: list[dict]

    # Missing Pages (Stub Creation)
    new_entities: list[str]
    new_concepts: list[str]

    missing_entities: list[str]
    missing_concepts: list[str]