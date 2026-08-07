from fastapi import APIRouter

from src.workflows.ingestion_workflow import workflow

router = APIRouter()


@router.post("/ingest")
def ingest(data: dict):

    state=workflow.invoke(
        {
            "source_path": data["source_path"]
        }
    )

    state["stats"] = {
        "summary_count": 1 if state.get("summary") else 0,
        "topic_count": 1 if state.get("document_name") else 0,
        "entity_count": len(state.get("entities", [])),
        "concept_count": len(state.get("concepts", [])),
        "document": state.get("document_name", "")
    }

    return {
        "status": "success",
        "message": "Document ingested successfully.",
        **state["stats"]
    }