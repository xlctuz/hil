from base.repositories import ProjectRepository
from base.models.project import Project


class DeleteProject:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def execute(self, project: Project):
        self.project_repository.delete_project(project)