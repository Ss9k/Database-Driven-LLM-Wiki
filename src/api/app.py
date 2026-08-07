from fastapi import FastAPI
from src.api.routes.query import router as query_router
from src.api.routes.ingest import router as ingest_router
from src.api.routes.health import router as health_router
from src.api.routes.workspace import router as workspace_router
from src.api.routes.wiki import router as wiki_router
from src.api.routes.dashboard import router as dashboard_router
app = FastAPI(
    title="Database Driven LLM Wiki",
    version="1.0"
)
app.include_router(query_router)
app.include_router(ingest_router)
app.include_router(health_router)
app.include_router(workspace_router)
app.include_router(wiki_router)
app.include_router(dashboard_router)