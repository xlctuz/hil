from domain.ports.project_repository_port import ProjectRepositoryPort
from domain.models.project import Project


class DeleteProject:
    def __init__(self, project_repository: ProjectRepositoryPort):
        self.project_repository = project_repository

    def execute(self, project: Project):
        self.project_repository.delete_project(project)