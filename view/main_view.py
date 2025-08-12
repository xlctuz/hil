from PySide6.QtCore import QObject, Property, Slot, QAbstractListModel, QModelIndex, Qt, Signal, QThread, QTimer
from view.project_model import ProjectModel
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine
from view.power_supply_proxy import PowerSupplyProxy
from core.project import Project
from core.power_supply_it6302 import Power_supply_it6302, Power_supply_it6302_channel, IO, Channel as PSChannel
from core.pcie_1762h_controller import Pcie_1762h, Pcie_1762h_do_channel, Pcie_1762h_di_channel, Status
from view.pcie_1762h_proxy import Pcie1762hProxy
from core.db import Session
from common.logger import logger


class ProjectProxy(QObject):
    def __init__(self, project_data, parent=None):
        super().__init__(parent)
        self._project_data = project_data
        self._power_supply = PowerSupplyProxy(project_data.power_supply if project_data else None, self)
        self._pcie_1762h = Pcie1762hProxy(project_data.pcie_1762h if project_data else None, self)

    @Property('QVariant', constant=True)
    def name(self):
        return self._project_data.name if self._project_data else None

    @Property(QObject, constant=True)
    def powerSupply(self):
        return self._power_supply

    @Property(QObject, constant=True)
    def pcie1762h(self):
        return self._pcie_1762h

class MainViewModel(QObject):
    currentProjectChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
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
        logger.info(f"Channel {index + 1} selected")
        session = Session()
        try:
            # Assuming channel IDs are 1, 2, 3...
            channel_id = index + 1
            projects = session.query(Project)\
                              .filter(Project.channel_id == channel_id)\
                              .options(joinedload(Project.power_supply)
                                       .joinedload(Power_supply_it6302.channels),
                                       joinedload(Project.pcie_1762h)
                                       .options(joinedload(Pcie_1762h.do_channels),
                                                joinedload(Pcie_1762h.di_channels))).all()
            self._project_model.set_projects(projects)
        finally:
            session.close()

        self._current_project = None
        self._current_project_proxy = ProjectProxy(None)
        self.currentProjectChanged.emit()
        if self._project_model.rowCount() > 0:
            self.selectProject(0)

    @Slot(int)
    def selectProject(self, index):
        project = self._project_model.get_project(index)
        if project:
            logger.info(f"Project {project.id} selected")
            self._current_project = project
            self._current_project_proxy = ProjectProxy(project)
            self._project_model.set_checked(index)
            self.currentProjectChanged.emit()
