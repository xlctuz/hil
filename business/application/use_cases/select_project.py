from business.domain.ports.project_repository_port import ProjectRepositoryPort
from business.domain.models.project import Project
from business.domain.models.channel import Channel
from typing import List


class SelectProject:
    def __init__(self, project_repository: ProjectRepositoryPort):
        self.project_repository = project_repository

    def execute(self, channel_index: int) -> List[Project]:
        # Create a channel object based on the index
        channel = Channel(channel_index)
        # Get projects for the selected channel
        projects = self.project_repository.get_projects_by_channel(channel)
        return projects