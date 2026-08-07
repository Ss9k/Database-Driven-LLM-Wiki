from pathlib import Path
import json
import shutil
from datetime import datetime
class ProjectManager:

    def __init__(self):

        self.projects_root = Path("projects")

        self.projects_root.mkdir(
            parents=True,
            exist_ok=True
        )
        self.active_project_file = Path("active_project.json")
        self.create_project("default")
        self.initialize_active_project()

    def project_path(self, name):

        return self.projects_root / name

    def exists(self, name):

        return self.project_path(name).exists()
    
    def create_project(self, name):

        root = self.project_path(name)

        folders = [

            root,

            root / "wiki",

            root / "wiki" / "entities",

            root / "wiki" / "concepts",

            root / "wiki" / "topics",

            root / "wiki" / "summaries",

            root / "faiss",

        ]

        for folder in folders:

            folder.mkdir(
                parents=True,
                exist_ok=True
            )
        metadata_file = root / "project.json"

        if not metadata_file.exists():

            metadata = self.create_metadata(name)

            self.save_metadata(
                name,
                metadata
            )
        return root
    
    def create_metadata(
    self,
    project_name,
    description=""):

        now = datetime.now().isoformat()

        return {

            "name": project_name,

            "created": now,

            "last_opened": now,

            "description": description

        }

    def save_metadata(
    self,
    project_name,
    metadata):

        project = self.project_path(project_name)

        metadata_file = project / "project.json"

        with open(
            metadata_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4
            )

    def load_metadata(self, project_name):

        metadata_file = (
            self.project_path(project_name)
            / "project.json"
        )

        with open(
            metadata_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)
        
    def update_last_opened(self, project_name):

        metadata = self.load_metadata(
            project_name
        )

        metadata["last_opened"] = (
            datetime.now().isoformat()
        )

        self.save_metadata(
            project_name,
            metadata
        )
    def initialize_active_project(self):

        if not self.active_project_file.exists():

            with open(
                self.active_project_file,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    {
                        "active": "default"
                    },
                    f,
                    indent=4
                )

    def get_active_project(self):

        with open(
            self.active_project_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)["active"]
        
    def set_active_project(self, project_name):

        if not self.exists(project_name):

            raise ValueError(
                f"Project '{project_name}' does not exist."
            )

        with open(
            self.active_project_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "active": project_name
                },
                f,
                indent=4
            )

        self.update_last_opened(
            project_name
        )

    @property
    def active_project(self):

        return self.get_active_project()
    
    def delete_project(self, project_name, confirm=False):

        if not confirm:
            raise ValueError(
                "Deletion requires confirm=True."
            )

        if project_name == self.active_project:
            raise ValueError(
                "Cannot delete active project."
            )

        project = self.project_path(project_name)

        if not project.exists():
            raise ValueError(
                "Project does not exist."
            )

        shutil.rmtree(project)

    # def switch_project(self, project_name):

    #     self.set_active_project(project_name)
    #     from src.workspace.workspace import workspace
    #     from src.database.metadata import metadata_db


    #     workspace.reload()

        # metadata_db.connect()