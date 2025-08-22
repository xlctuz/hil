from PySide6.QtCore import QObject, Property, Slot, Signal
from core.entities.project import Project
from adapters.views.common.project_list_view_model import ProjectListViewModel
from adapters.views.main.project_view_model import ProjectViewModel
from typing import List
from core.logger import logger
from core.usecases import UseCases

class MainViewModel(QObject):
    currentProjectChanged = Signal()

    def __init__(self, usecases: UseCases, parent=None):
        super().__init__(parent)
        self.usecases = usecases
        self._project_model = ProjectListViewModel()
        self._current_project = None
        self._current_project_proxy = ProjectViewModel(None)
        self._current_channel_index = 0

    @Property(QObject, constant=True)
    def projectsModel(self):
        return self._project_model

    @Property(QObject, notify=currentProjectChanged)
    def currentProject(self):
        return self._current_project_proxy

    @Slot(int)
    def selectChannel(self, index):
        self._current_channel_index = index
        logger.info(f"Channel {index + 1} selected")

        # Use the use case to get projects for the selected channel
        projects = self.usecases.select_project_from_channel(index)
        logger.info(f"{projects}")
        self._project_model.set_projects(projects)

        self._current_project = None
        self._current_project_proxy = ProjectViewModel(None)
        self.currentProjectChanged.emit()
        if self._project_model.rowCount() > 0:
            self.selectProject(0)

    @Slot(int)
    def selectProject(self, index):
        project = self._project_model.get_project(index)
        if project:
            logger.info(f"Project {project.id} selected")
            self._current_project = project
            self._current_project_proxy = ProjectViewModel(project)
            self._project_model.set_checked(index)
            self.currentProjectChanged.emit()
