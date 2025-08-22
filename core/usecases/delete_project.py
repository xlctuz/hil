from core.repositories import ProjectRepository
from core.entities.project import Project
from core.logger import logger


class Delete_project:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def __call__(self, project: Project) -> None:
        logger.info(f"Deleting project {project.name} (ID: {project.id})")
        self.project_repository.delete_project(project)