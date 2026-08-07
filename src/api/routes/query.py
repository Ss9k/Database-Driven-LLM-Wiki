from fastapi import APIRouter

from src.workflows.query_workflow import workflow

router = APIRouter()


@router.post("/query")
def query(data: dict):

    result = workflow.invoke(
        {
            "question": data["question"]
        }
    )

    return {
        "answer": result["answer"],
        "sources": result["sources"],
    }