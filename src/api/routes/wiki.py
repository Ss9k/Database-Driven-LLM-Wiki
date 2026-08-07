from pathlib import Path

from fastapi import APIRouter, HTTPException
from src.workspace.workspace import workspace

router = APIRouter()


@router.get("/wiki")
def browse_wiki(category: str):

    mapping = {
        "entities": workspace.entities,
        "concepts": workspace.concepts,
        "topics": workspace.topics,
        "summaries": workspace.summaries,
    }

    if category not in mapping:
        raise HTTPException(
            status_code=400,
            detail="Invalid category."
        )

    folder = mapping[category]

    pages = sorted(
        [p.stem for p in folder.glob("*.md")]
    )

    return {
        "pages": pages
    }


@router.get("/wiki/page")
def get_page(category: str, page: str):

    mapping = {
        "entities": workspace.entities,
        "concepts": workspace.concepts,
        "topics": workspace.topics,
        "summaries": workspace.summaries,
    }

    if category not in mapping:
        raise HTTPException(
            status_code=400,
            detail="Invalid category."
        )

    file = mapping[category] / f"{page}.md"

    if not file.exists():
        raise HTTPException(
            status_code=404,
            detail="Page not found."
        )

    return {
        "title": page,
        "content": file.read_text(
            encoding="utf-8"
        )
    }