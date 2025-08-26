import sys
import os
from PySide6.QtCore import QObject, Property, Slot, Signal
from core.logger import logger
import traceback

# Add project root to path to import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from core.entities.power_supply import PowerSupply
from core.entities.pcie_1762h import Pcie1762h
from adapters.devices.visa_resource_manager import rm
from adapters.views.common.project_list_view_model import ProjectListViewModel
from adapters.views.config.project_config_view_model import ProjectConfigViewModel
from core.usecases import UseCases
from core.interfaces.scheduler_port import SchedulerPort

class ConfigViewModel(QObject):
    currentChannelChanged = Signal(int)
    currentProjectChanged = Signal()
    powerSupplyTestFailed = Signal(str)
    powerSupplyDataUpdated = Signal(list, list, list) # voltage, current, power

    def __init__(self, usecases: UseCases, power_supply_adapter, parent=None):
        super().__init__(parent)
        self.usecases = usecases
        self.power_supply_adapter = power_supply_adapter
        self._test_scheduler = None

        self._project_model = ProjectListViewModel()
        self._current_project = None
        # self._current_project_proxy = ProjectConfigViewModel(usecases, None)
        self._current_project_proxy = None
        self._current_channel_index = 0
        self._is_testing = False

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
        self.usecases.configure_power_supply(
            self._current_project.power_supply,
            resource_name,
            baud_rate
        )

        self.usecases.save_project(self._current_project)

        self._current_project_proxy.powerSupply.resourceNameChanged.emit()
        self._current_project_proxy.powerSupply.baudRateChanged.emit()

    @Slot(int)
    def selectChannel(self, index):
        self._current_channel_index = index
        logger.info(f"Channel {index} selected")

        # Use the use case to get projects for the selected channel
        projects = self.usecases.select_project_from_channel(index)
        self._project_model.set_projects(projects)

        self._current_project = None
        # self._current_project_proxy = ProjectConfigViewModel(self.usecases, None)
        self._current_project_proxy = None
        self.currentProjectChanged.emit()
        if self._project_model.rowCount() > 0:
            self.selectProject(0)

    @Slot(str)
    def addProject(self, name):
        if not name:
            return

        logger.info(f"Adding project {name} to channel {self._current_channel_index + 1}")

        # Use the use case to add a new project
        self.usecases.add_project(name, self._current_channel_index)

        # Refresh the project list
        self.selectChannel(self._current_channel_index)

    @Slot(int, float)
    def setPowerSupplyVoltage(self, channel_index, voltage):
        if not self._current_project or not self._current_project.power_supply:
            return

        # Use the use case to set the voltage
        self.usecases.set_power_supply_voltage(
            self._current_project.power_supply,
            channel_index,
            voltage
        )

        self.usecases.save_project(self._current_project)

        # Update UI
        self.currentProjectChanged.emit()

    @Slot(int, float)
    def setPowerSupplyCurrent(self, channel_index, current):
        if not self._current_project or not self._current_project.power_supply:
            return

        # Use the use case to set the current
        self.usecases.set_power_supply_current(
            self._current_project.power_supply,
            channel_index,
            current
        )

        self.usecases.save_project(self._current_project)

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

        # Store the testing state
        self._is_testing = testing

        if testing:
            # Start monitoring using the use case
            try:
                self._test_scheduler = self.usecases.start_power_supply_monitoring(
                    self._current_project,
                    self._on_power_supply_data_updated,
                    self.powerSupplyTestFailed.emit
                )
            except Exception as e:
                msg = f"启动电源监控失败: {str(e)}"
                logger.info(msg)
                self.powerSupplyTestFailed.emit(msg)
                return
        else:
            # Stop monitoring using the use case
            try:
                self.usecases.stop_power_supply_monitoring(self._test_scheduler)
                self._test_scheduler = None
            except Exception as e:
                msg = f"停止电源监控失败: {str(e)}"
                logger.info(msg)
                self.powerSupplyTestFailed.emit(msg)
                return

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
        self.usecases.reset_power_supply_settings(self._current_project.power_supply)

        self.usecases.save_project(self._current_project)

        # Update UI
        self.currentProjectChanged.emit()

    @Slot()
    def deleteCurrentProject(self):
        if not self._current_project:
            logger.info("No project selected to delete.")
            return

        logger.info(f"Deleting project {self._current_project.name} (ID: {self._current_project.id})")

        # Use the use case to delete the project
        self.usecases.delete_project(self._current_project)

        # Refresh the project list for the current channel
        self.selectChannel(self._current_channel_index)

    def _on_project_saved(self):
        """Slot to refresh the project list when a project is saved."""
        logger.info("Project saved, refreshing project list.")
        current_index = self._project_model.get_checked_index()
        self.selectChannel(self._current_channel_index)
        # re-select the same project index if it's still valid
        if current_index < self._project_model.rowCount():
            self.selectProject(current_index)

    @Slot(int)
    def selectProject(self, index):
        project = self._project_model.get_project(index)
        if project:
            # Disconnect from the previous proxy's signal if it exists
            if self._current_project_proxy and self._current_project_proxy._project_data:
                try:
                    self._current_project_proxy.projectSaved.disconnect(self._on_project_saved)
                except RuntimeError:
                    pass  # This happens if the signal was not connected, which is fine

            logger.info(f"Project {project.id} selected")
            self._current_project = project
            self._current_project_proxy = ProjectConfigViewModel(self.usecases, project)

            # Connect the new proxy's signal
            self._current_project_proxy.projectSaved.connect(self._on_project_saved)

            self._project_model.set_checked(index)
            self.currentProjectChanged.emit()
