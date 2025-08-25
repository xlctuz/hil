from PySide6.QtCore import QObject, Property, Slot, Signal, QThread, QTimer
from adapters.views.config.power_supply_config_view_model import PowerSupplyConfigViewModel
from adapters.views.config.pcie_1762h_config_view_model import Pcie1762hConfigViewModel
from adapters.views.config.pci1720u_config_view_model import Pci1720uConfigViewModel
from core.entities.power_supply import IO
from core.entities.pcie_1762h import Status
from core.logger import logger
from core.usecases import UseCases


class ProjectConfigViewModel(QObject):
    # Signals for communicating with UI
    voltageDataChanged = Signal(list)
    currentDataChanged = Signal(list)
    powerDataChanged = Signal(list)
    dioDataChanged = Signal(int)
    errorOccurred = Signal(str)
    started = Signal()
    stopped = Signal()
    nameChanged = Signal()
    projectSaved = Signal()

    def __init__(self, usecases: UseCases, project_data, parent=None):
        super().__init__(parent)
        self.usecases = usecases
        self._project_data = project_data
        self._power_supply = PowerSupplyConfigViewModel(usecases, project_data.power_supply if project_data else None, self)
        self._pcie_1762h = Pcie1762hConfigViewModel(usecases, project_data.pcie_1762h if project_data else None, self)
        self._pci1720u = Pci1720uConfigViewModel(usecases, project_data.pci1720u if project_data else None, self)
        self._is_started = False

    @Property('QVariant', notify=nameChanged)
    def name(self):
        return self._project_data.name if self._project_data else None

    @name.setter
    def name(self, value):
        if self._project_data and self._project_data.name != value:
            self._project_data.name = value
            self.usecases.save_project(self._project_data)
            self.nameChanged.emit()
            self.projectSaved.emit()

    @Property(QObject, constant=True)
    def powerSupply(self):
        return self._power_supply

    @Property(QObject, constant=True)
    def pcie1762h(self):
        return self._pcie_1762h

    @Property(QObject, constant=True)
    def pci1720u(self):
        return self._pci1720u

    @Property(bool, constant=True)
    def is_started(self):
        return self._is_started

    
