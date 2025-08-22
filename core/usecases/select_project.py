from typing import List
from core.repositories import ProjectRepository
from core.entities.project import Project
from core.logger import logger


class SelectProject:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def __call__(self, channel_index: int) -> List[Project]:
        logger.info(f"Selecting projects on channel {channel_index}")
        # Get projects for the selected channel
        projects = self.project_repository.get_projects_by_channel(channel_index)

        return projects