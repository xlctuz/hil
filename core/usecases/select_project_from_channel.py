from typing import List
from core.database import Session
from sqlalchemy import select
from core.logger import logger
from core.entities.project import Project
from core.entities.channel import Channel
from core.repositories import ProjectRepository


class Select_project_from_channel:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def __call__(self, channel_index: int) -> List[Project]:
        return self.project_repository.get_projects_by_channel(channel_index)
