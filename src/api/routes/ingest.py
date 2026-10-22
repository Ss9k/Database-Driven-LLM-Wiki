# from fastapi import APIRouter

# from src.workflows.ingestion_workflow import workflow

# router = APIRouter()


# @router.post("/ingest")
# def ingest(data: dict):

#     state=workflow.invoke(
#         {
#             "source_path": data["source_path"]
#         }
#     )

#     state["stats"] = {
#         "summary_count": 1 if state.get("summary") else 0,
#         "topic_count": 1 if state.get("document_name") else 0,
#         "entity_count": len(state.get("entities", [])),
#         "concept_count": len(state.get("concepts", [])),
#         "document": state.get("document_name", "")
#     }

#     return {
#         "status": "success",
#         "message": "Document ingested successfully.",
#         **state["stats"]
#     }

from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import APIRouter, UploadFile, File, HTTPException

from src.workflows.ingestion_workflow import workflow

router = APIRouter()

ALLOWED_EXTENSIONS = {".md", ".txt"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    filename = Path(file.filename or "").name

    if not filename or Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only .md and .txt files are supported.",
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(status_code=400, detail="The file is empty.")

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Maximum file size is 5 MB.",
        )

    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must use UTF-8 encoding.",
        )

    try:
        with TemporaryDirectory(prefix="wiki_ingest_") as temp_dir:
            source_path = Path(temp_dir) / filename
            source_path.write_text(text, encoding="utf-8")

            state = workflow.invoke({
                "source_path": str(source_path)
            })

        stats = {
            "summary_count": 1 if state.get("summary") else 0,
            "topic_count": 1 if state.get("document_name") else 0,
            "entity_count": len(state.get("entities", [])),
            "concept_count": len(state.get("concepts", [])),
            "document": state.get("document_name", ""),
        }

        return {
            "status": "success",
            "message": "Document ingested successfully.",
            **stats,
        }

    except HTTPException:
        raise
    except Exception:
        # Keep detailed exception information in server logs.
        import logging
        logging.exception("Document ingestion failed")
        raise HTTPException(
            status_code=500,
            detail="Document ingestion failed. Check backend logs.",
        )
    finally:
        await file.close()
