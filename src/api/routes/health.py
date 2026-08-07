# from fastapi import APIRouter

# from src.utils.broken_link_detector import BrokenLinkDetector
# from src.utils.orphan_page_detector import OrphanPageDetector
# from src.utils.duplicate_detector import DuplicateDetector
# from src.workspace.workspace import workspace
# router = APIRouter()

# def count_pages(folder):
#     return len(list(folder.glob("*.md")))

# @router.get("/health")
# def health():

#     broken = BrokenLinkDetector().detect()

#     orphan = OrphanPageDetector().detect()

#     duplicate = DuplicateDetector().detect()

#     return {
#         "broken_links": broken,
#         "orphan_pages": orphan,
#         "duplicate_pages": duplicate,
#         "entities": count_pages(workspace.entities),
#         "concepts": count_pages(workspace.concepts),
#         "topics": count_pages(workspace.topics),
#         "summaries": count_pages(workspace.summaries),
#         "current_workspace": workspace.project_manager.active_project,
#         "total_documents": count_pages(workspace.summaries)
#     }

from fastapi import APIRouter

from src.utils.broken_link_detector import BrokenLinkDetector
from src.utils.orphan_page_detector import OrphanPageDetector
from src.utils.duplicate_detector import DuplicateDetector
from src.workspace.workspace import workspace

router = APIRouter()


def count_pages(folder):
    return len(list(folder.glob("*.md")))


@router.get("/health")
def health():

    result = {}

    try:
        result["broken_links"] = BrokenLinkDetector().detect()
    except Exception as e:
        result["broken_links"] = f"ERROR: {repr(e)}"

    try:
        result["orphan_pages"] = OrphanPageDetector().detect()
    except Exception as e:
        result["orphan_pages"] = f"ERROR: {repr(e)}"

    try:
        result["duplicate_pages"] = DuplicateDetector().detect()
    except Exception as e:
        result["duplicate_pages"] = f"ERROR: {repr(e)}"

    try:
        result["entities"] = count_pages(workspace.entities)
        result["concepts"] = count_pages(workspace.concepts)
        result["topics"] = count_pages(workspace.topics)
        result["summaries"] = count_pages(workspace.summaries)
        result["current_workspace"] = workspace.project_manager.active_project
        result["total_documents"] = count_pages(workspace.summaries)
    except Exception as e:
        result["workspace_error"] = repr(e)

    return result