import sys
import os
from PySide6.QtCore import QObject, Property, Slot, Signal
from base.logger import logger
import traceback

# Add project root to path to import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from base.models.power_supply import PowerSupply
from base.models.pcie_1762h import Pcie1762h
from base.devices.visa_resource_manager import rm
from ui.project_model import ProjectModel
from ui.project_proxy import ProjectProxy
from core.use_cases.project_management import ProjectManagement
from core.use_cases.power_supply_management import PowerSupplyConfiguration


class ConfigViewModel(QObject):
    currentChannelChanged = Signal(int)
    currentProjectChanged = Signal()
    powerSupplyTestFailed = Signal(str)
    powerSupplyDataUpdated = Signal(list, list, list) # voltage, current, power

    def __init__(self, project_management_use_case: ProjectManagement,
                 power_supply_configuration_use_case: PowerSupplyConfiguration,
                 power_supply_adapter, power_supply_polling_service,
                 parent=None):
        super().__init__(parent)
        self.project_management_use_case = project_management_use_case
        self.power_supply_configuration_use_case = power_supply_configuration_use_case
        self.power_supply_adapter = power_supply_adapter
        self.power_supply_polling_service = power_supply_polling_service

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

    @Property('QVariant', constant=True)
    def availableVisaResources(self):
        try:
            return list(rm.list_resources())
        except Exception as e:
            logger.info(f"Could not list VISA resources: {e}")
            return []

    @Slot(str, int)
    def setPowerSupplyConfig(self, resource_name, baud_rate):
        if not self._current_project or not self._current_project.power_supply:
            return

        # Use the use case to configure the power supply
        self.power_supply_configuration_use_case.configure_power_supply(
            self._current_project.power_supply,
            resource_name,
            baud_rate
        )

        self.project_management_use_case.save_project(self._current_project)

        self._current_project_proxy.powerSupply.resourceNameChanged.emit()
        self._current_project_proxy.powerSupply.baudRateChanged.emit()

    @Slot(int)
    def selectChannel(self, index):
        self._current_channel_index = index
        logger.info(f"Channel {index + 1} selected")

        # Use the use case to get projects for the selected channel
        projects = self.project_management_use_case.select_project(index)
        self._project_model.set_projects(projects)

        self._current_project = None
        self._current_project_proxy = ProjectProxy(None)
        self.currentProjectChanged.emit()
        if self._project_model.rowCount() > 0:
            self.selectProject(0)

    @Slot(str)
    def addProject(self, name):
        if not name:
            return

        logger.info(f"Adding project {name} to channel {self._current_channel_index + 1}")

        # Use the use case to add a new project
        self.project_management_use_case.add_project(name, self._current_channel_index)

        # Refresh the project list
        self.selectChannel(self._current_channel_index)

    @Slot(int, float)
    def setPowerSupplyVoltage(self, channel_index, voltage):
        if not self._current_project or not self._current_project.power_supply:
            return

        # Use the use case to set the voltage
        self.power_supply_configuration_use_case.set_power_supply_voltage(
            self._current_project.power_supply,
            channel_index,
            voltage
        )

        self.project_management_use_case.save_project(self._current_project)

        # Update UI
        self.currentProjectChanged.emit()

    @Slot(int, float)
    def setPowerSupplyCurrent(self, channel_index, current):
        if not self._current_project or not self._current_project.power_supply:
            return

        # Use the use case to set the current
        self.power_supply_configuration_use_case.set_power_supply_current(
            self._current_project.power_supply,
            channel_index,
            current
        )

        self.project_management_use_case.save_project(self._current_project)

        # Update UI
        self.currentProjectChanged.emit()

    @Slot(bool)
    def togglePowerSupplyTest(self, testing):
        logger.info(f"toggle power supply test")
        if not self._current_project or not self._current_project.power_supply:
            msg = "没有为测试选择项目."
            logger.info(msg)
            self.powerSupplyTestFailed.emit(msg)
            return

        ps_config = self._current_project.power_supply
        if not ps_config.resource_name:
            msg = "电源资源名称未配置."
            logger.info(msg)
            self.powerSupplyTestFailed.emit(msg)
            return

        # Use the use case to toggle the test
        self.power_supply_configuration_use_case.toggle_power_supply_test(
            ps_config,
            self._current_project,
            testing,
            self.power_supply_adapter,
            self.power_supply_polling_service,
            self._on_power_supply_data_updated,
            self.powerSupplyTestFailed.emit
        )

    @Slot(dict)
    def _on_power_supply_data_updated(self, data):
        logger.info(f"on power supply data updated {data['voltage']}, {data['current']}, {data['power']}")
        self.powerSupplyDataUpdated.emit(data['voltage'], data['current'], data['power'])

    @Slot()
    def resetPowerSupplySettings(self):
        if not self._current_project or not self._current_project.power_supply:
            logger.info("No project or power supply selected.")
            return

        logger.info(f"Resetting power supply settings for project {self._current_project.name}")

        # Use the use case to reset the settings
        self.power_supply_configuration_use_case.reset_power_supply_settings(self._current_project.power_supply)

        self.project_management_use_case.save_project(self._current_project)

        # Update UI
        self.currentProjectChanged.emit()

    @Slot()
    def deleteCurrentProject(self):
        if not self._current_project:
            logger.info("No project selected to delete.")
            return

        logger.info(f"Deleting project {self._current_project.name} (ID: {self._current_project.id})")

        # Use the use case to delete the project
        self.project_management_use_case.delete_project(self._current_project)

        # Refresh the project list for the current channel
        self.selectChannel(self._current_channel_index)

    @Slot(int)
    def selectProject(self, index):
        project = self._project_model.get_project(index)
        if project:
            logger.info(f"Project {project.id} selected")
            self._current_project = project
            self._current_project_proxy = ProjectProxy(project)
            self._project_model.set_checked(index)
            self.currentProjectChanged.emit()
