from PySide6.QtCore import QObject, Property, Slot, Signal
from core.use_cases.select_project import SelectProject
from base.models.project import Project
from base.models.channel import Channel
from ui.project_model import ProjectModel
from ui.project_proxy import ProjectProxy
from typing import List


class MainViewModel(QObject):
    currentProjectChanged = Signal()

    def __init__(self, select_project_use_case: SelectProject, parent=None):
        super().__init__(parent)
        self.select_project_use_case = select_project_use_case
        self._project_model = ProjectModel()
        self._current_project = None
        self._current_project_proxy = ProjectProxy(None)
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
        print(f"Channel {index + 1} selected")
        
        # Use the use case to get projects for the selected channel
        projects = self.select_project_use_case.execute(index)
        self._project_model.set_projects(projects)

        self._current_project = None
        self._current_project_proxy = ProjectProxy(None)
        self.currentProjectChanged.emit()
        if self._project_model.rowCount() > 0:
            self.selectProject(0)

    @Slot(int)
    def selectProject(self, index):
        project = self._project_model.get_project(index)
        if project:
            print(f"Project {project.id} selected")
            self._current_project = project
            self._current_project_proxy = ProjectProxy(project)
            self._project_model.set_checked(index)
            self.currentProjectChanged.emit()