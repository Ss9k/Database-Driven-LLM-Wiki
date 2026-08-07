from pathlib import Path
from langgraph.graph import StateGraph, END
from src.workflows.state import WikiState
from src.agents.extraction_agent import ExtractionAgent
from src.utils.wiki_manager import (
    create_or_update_summary_page,
    create_or_update_entity_page,
    create_or_update_concept_page,
    create_or_update_topic_page,
    update_index,
    log_activity,
)
from src.utils.broken_link_detector import BrokenLinkDetector
from src.utils.contradiction_checker import ContradictionChecker
from src.utils.gap_detector import GapDetector
from src.embeddings.embedding_generator import EmbeddingGenerator
from src.vectorstore.faiss_store import faiss_store
from src.database.metadata import metadata_db
from src.utils.orphan_page_detector import OrphanPageDetector
from src.utils.duplicate_detector import DuplicateDetector
from src.utils.wiki_health_report import WikiHealthReport
from src.utils.interactive_fixer import InteractiveFixer
from src.workspace.workspace import workspace
from src.agents.summary_agent import SummaryAgent
from src.agents.entity_enrichment_agent import EntityEnrichmentAgent
from src.utils.context_extractor import ContextExtractor
from src.agents.concept_enrichment_agent import ConceptEnrichmentAgent
from src.agents.extraction_agent import ExtractionAgent

extraction_agent = ExtractionAgent()
summary_agent = SummaryAgent()
entity_agent = EntityEnrichmentAgent()
checker = ContradictionChecker()
gap_detector = GapDetector()
broken_detector = BrokenLinkDetector()
embedding_generator = EmbeddingGenerator()
orphan_detector = OrphanPageDetector()
duplicate_detector = DuplicateDetector()
health_report = WikiHealthReport()
interactive_fixer = InteractiveFixer()
context_extractor = ContextExtractor()
concept_agent = ConceptEnrichmentAgent()
faiss_store.load()

# --------------------------------------------------
# Read Source
# --------------------------------------------------

def read_source_node(state: WikiState):

    path = Path(state["source_path"])

    state["source_text"] = path.read_text(
        encoding="utf-8"
    )

    state["document_name"] = path.stem

    return state


# --------------------------------------------------
# Extract Information
# --------------------------------------------------

def extract_node(state: WikiState):
    
    result = extraction_agent.extract(
        state["source_text"]
    )
    print("\n========== EXTRACTION ==========")
    print(result)
    print("================================")
    
    state["entities"] = result["entities"]
    state["concepts"] = result["concepts"]
    state["claims"] = result["claims"]

    return state

def gap_node(state: WikiState):

    gaps = gap_detector.detect(

        state["entities"],

        state["concepts"],

        state["document_name"]

    )

    state["missing_entities"] = gaps["entities"]

    state["missing_concepts"] = gaps["concepts"]

    return state
# --------------------------------------------------
# Summary
# --------------------------------------------------

def summary_node(state: WikiState):
    summary = summary_agent.generate(
        state["source_text"]
    )

    state["summary"] = summary
    create_or_update_summary_page(
        state["document_name"],
        summary,
        state["document_name"]
    )

    return state


# --------------------------------------------------
# Entities
# --------------------------------------------------

def entity_node(state: WikiState):

    for entity in state["entities"]:

        context = context_extractor.extract(
            state["source_text"],
            entity
        )
        print(f"\n========== {entity} ==========")
        print(context)
        print("================================")

        summary = entity_agent.enrich(
            entity,
            context
        )

        if summary.strip().upper() == "NOT_ENOUGH_INFORMATION":

            summary = (
                f"No detailed information about {entity} "
                f"was found in this document."
            )

        create_or_update_entity_page(

            entity,
            summary,
            state["document_name"]
        )

    return state


# --------------------------------------------------
# Concepts
# --------------------------------------------------

def concept_node(state: WikiState):

    for concept in state["concepts"]:

        context = context_extractor.extract(
            state["source_text"],
            concept
        )
        print(f"\n========== {concept} ==========")
        print(context)
        print("================================")

        summary = concept_agent.enrich(
            concept,
            context
        )

        if summary.strip().upper() in (
            "NOT_ENOUGH_INFORMATION",
            "UNKNOWN"
        ):

            summary = (
                f"The document mentions '{concept}' "
                f"but does not provide enough information "
                f"to define it."
            )

        create_or_update_concept_page(
            concept,
            summary,
            state["document_name"]
        )

    return state


def topic_node(state: WikiState):

    create_or_update_topic_page(

        state["document_name"],

        state["entities"],

        state["concepts"],

        state["document_name"],

        state["document_name"]

    )

    return state
# --------------------------------------------------
# Contradictions
# --------------------------------------------------

def contradiction_node(state: WikiState):

    pages = state["entities"] + state["concepts"]

    for page in pages:

        checker.check(
            page,
            state["claims"]
        )

    return state


def embedding_sync_node(state: WikiState):
    embedding_generator.reload()
    faiss_store.reload()
    metadata_db.connect()

    modified_pages = embedding_generator.get_modified_pages()

    if not modified_pages:
        return state

    embeddings = embedding_generator.generate_all_embeddings()

    embedding_map = {
        page["path"]: page
        for page in embeddings
    }

    for page in modified_pages:

        page_data = embedding_map.get(str(page["path"]))

        if page_data:

            faiss_store.update_page(page_data)

    return state

def broken_link_node(state: WikiState):

    broken = broken_detector.detect()

    state["broken_links"] = broken

    if broken:

        print("\nBroken Links Found:")

        for item in broken:

            print(
                f"{item['page']} -> {item['broken_link']}"
            )

    return state

def orphan_page_node(state: WikiState):

    orphan = orphan_detector.detect()

    state["orphan_pages"] = orphan

    if orphan:

        print("\nOrphan Pages:")

        for page in orphan:

            print(page)

    return state

def duplicate_page_node(state: WikiState):

    duplicates = duplicate_detector.detect()

    state["duplicate_pages"] = duplicates

    if duplicates:

        print("\nDuplicate Pages:")

        for item in duplicates:

            print(
                f"{item['page1']} <-> {item['page2']} ({item['score']})"
            )

    return state

def health_report_node(state: WikiState):

    report = health_report.generate(

        state.get("broken_links", []),

        state.get("orphan_pages", []),

        state.get("duplicate_pages", []),

    )

    report_path = (
        workspace.project_root
        / "wiki_health_report.md"
    )

    report_path.write_text(

        report,

        encoding="utf-8"

    )

    print(
        "\nWiki Health Report Updated"
    )

    return state

def interactive_fix_node(state: WikiState):

    broken = state.get("broken_links", [])

    if broken:

        interactive_fixer.fix_broken_links(broken)

    return state
# --------------------------------------------------
# Index
# --------------------------------------------------

def index_node(state: WikiState):

    update_index()

    return state


# --------------------------------------------------
# Log
# --------------------------------------------------

def log_node(state: WikiState):
    # update_index() 
    log_activity(
        f"Ingestion completed: {state['document_name']}"
    )

    return state


# --------------------------------------------------
# Workflow
# --------------------------------------------------

def build_workflow():

    builder = StateGraph(WikiState)

    builder.add_node("read", read_source_node)

    builder.add_node("extract", extract_node)

    builder.add_node("summary", summary_node)

    builder.add_node("entity", entity_node)

    builder.add_node("concept", concept_node)

    builder.add_node("contradiction", contradiction_node)
    
    builder.add_node("gap",gap_node)

    builder.add_node("topic", topic_node)
    
    builder.add_node("embedding_sync", embedding_sync_node)

    builder.add_node("broken_links", broken_link_node)
    
    builder.add_node("orphan_pages", orphan_page_node)
    
    builder.add_node("duplicate_pages", duplicate_page_node)
    
    builder.add_node("health_report", health_report_node)
    
    builder.add_node("interactive_fix", interactive_fix_node)
    
    builder.add_node("index", index_node)

    builder.add_node("log", log_node)

    builder.set_entry_point("read")

    builder.add_edge("read", "extract")

    builder.add_edge("extract", "gap")

    builder.add_edge("gap", "summary")

    builder.add_edge("summary", "entity")

    builder.add_edge("entity", "concept")

    builder.add_edge("concept", "topic")

    builder.add_edge("topic", "contradiction")

    builder.add_edge("contradiction", "embedding_sync")

    builder.add_edge("embedding_sync", "broken_links")

    builder.add_edge("broken_links", "orphan_pages")
    
    builder.add_edge("orphan_pages", "duplicate_pages")
    
    builder.add_edge("duplicate_pages", "health_report")

    builder.add_edge("health_report", "interactive_fix")
    
    builder.add_edge("interactive_fix", "index")
    
    builder.add_edge("index", "log")

    builder.add_edge("log", END)

    return builder.compile()

workflow = build_workflow()