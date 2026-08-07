from fastapi import APIRouter

from src.workspace.workspace import workspace

router = APIRouter()


def count_pages(folder):
    return len(list(folder.glob("*.md")))


@router.get("/dashboard")
def dashboard():

    return {
        "entities": count_pages(workspace.entities),
        "concepts": count_pages(workspace.concepts),
        "topics": count_pages(workspace.topics),
        "summaries": count_pages(workspace.summaries),

        "current_workspace": workspace.project_manager.active_project,

        "total_documents": count_pages(workspace.summaries),
    }