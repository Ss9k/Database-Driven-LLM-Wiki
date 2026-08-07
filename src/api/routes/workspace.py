from fastapi import APIRouter, HTTPException
from src.project.project_manager import ProjectManager
from src.workspace.workspace import workspace
from pathlib import Path
from pydantic import BaseModel
router = APIRouter()


class ProjectRequest(BaseModel):
    name: str

@router.get("/projects")
def projects():

    root = Path("projects")

    return {
        "projects":[
            p.name
            for p in root.iterdir()
            if p.is_dir()
        ]
    }

@router.post("/projects/create")
def create_project(request: ProjectRequest):

    name = request.name.strip()

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Project name required."
        )

    if workspace.project_manager.exists(name):
        raise HTTPException(
            status_code=400,
            detail="Project already exists."
        )

    workspace.project_manager.create_project(name)

    return {
        "status": "success",
        "message": f"{name} created."
    }

@router.post("/projects/switch")
def switch_workspace(request: ProjectRequest):

    try:

        workspace.switch_project(request.name)

        return {
            "status": "success",
            "message": f"Switched to {request.name}"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    
@router.delete("/projects/{name}")
def delete_project(name: str):

    if name == workspace.project_name:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete active project."
        )

    try:

        workspace.project_manager.delete_project(
            name,
            confirm=True
        )

        return {
            "status": "success",
            "message": f"{name} deleted."
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )