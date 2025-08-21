from abc import ABC, abstractmethod
from domain.models.project import Project
from domain.models.channel import Channel
from typing import List


class ProjectRepositoryPort(ABC):
    @abstractmethod
    def get_projects_by_channel(self, channel: Channel) -> List[Project]:
        pass

    @abstractmethod
    def get_project_by_id(self, project_id: int) -> Project:
        pass

    @abstractmethod
    def save_project(self, project: Project):
        pass

    @abstractmethod
    def delete_project(self, project: Project):
        pass

    @abstractmethod
    def create_channels(self):
        pass

    @abstractmethod
    def get_channels(self) -> List[Channel]:
        pass