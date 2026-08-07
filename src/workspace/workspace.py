from pathlib import Path

from src.project.project_manager import ProjectManager


class Workspace:

    def __init__(self):

        self.project_manager = ProjectManager()

        self.reload()

    def reload(self):

        project = self.project_manager.active_project

        root = (
            self.project_manager
            .project_path(project)
        )
        self.project_name = project
        
        self.project_root = root

        self.wiki = root / "wiki"

        self.entities = self.wiki / "entities"

        self.concepts = self.wiki / "concepts"

        self.topics = self.wiki / "topics"

        self.summaries = self.wiki / "summaries"

        self.faiss = root / "faiss"

        self.database = root / "metadata.db"

    def switch_project(self, project_name):

        self.project_manager.set_active_project(project_name)

        self.reload_managers()
    
    def reload_managers(self):

        self.reload()
        from src.database.metadata import metadata_db
        from src.vectorstore.faiss_store import faiss_store

        metadata_db.connect()

        faiss_store.reload()

        faiss_store.load()
        

workspace = Workspace()