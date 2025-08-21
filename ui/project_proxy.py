from PySide6.QtCore import QObject, Property, Slot, Signal
from ui.power_supply_proxy import PowerSupplyProxy
from ui.pcie_1762h_proxy import Pcie1762hProxy


class ProjectProxy(QObject):
    def __init__(self, project_data, parent=None):
        super().__init__(parent)
        self._project_data = project_data
        self._power_supply = PowerSupplyProxy(project_data.power_supply if project_data else None, self)
        self._pcie_1762h = Pcie1762hProxy(project_data.pcie_1762h if project_data else None, self)
        self._is_started = False

    @Property('QVariant', constant=True)
    def name(self):
        return self._project_data.name if self._project_data else None

    @Property(QObject, constant=True)
    def powerSupply(self):
        return self._power_supply

    @Property(QObject, constant=True)
    def pcie1762h(self):
        return self._pcie_1762h

    @Property(bool, constant=True)
    def is_started(self):
        return self._is_started

    @Slot()
    def start(self):
        # TODO: Implement project start logic
        self._is_started = True

    @Slot()
    def stop(self):
        # TODO: Implement project stop logic
        self._is_started = False