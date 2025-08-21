import sys
import os
from PySide6.QtCore import QObject, Property, Slot, Signal
from common.logger import logger
import traceback

# Add project root to path to import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

from business.domain.models.power_supply import PowerSupply
from business.domain.models.pcie_1762h import Pcie1762h
from enum import Enum
from data_access.hardware.visa_resource_manager import rm
from presentation.ui.project_model import ProjectModel
from presentation.ui.project_proxy import ProjectProxy
from business.application.use_cases.select_project import SelectProject
from business.application.use_cases.configure_power_supply import ConfigurePowerSupply
from business.application.use_cases.add_project import AddProject
from business.application.use_cases.delete_project import DeleteProject
from business.application.use_cases.set_power_supply_voltage import SetPowerSupplyVoltage
from business.application.use_cases.set_power_supply_current import SetPowerSupplyCurrent
from business.application.use_cases.reset_power_supply_settings import ResetPowerSupplySettings
from business.application.use_cases.toggle_power_supply_test import TogglePowerSupplyTest


class ConfigViewModel(QObject):
    currentChannelChanged = Signal(int)
    currentProjectChanged = Signal()
    powerSupplyTestFailed = Signal(str)
    powerSupplyDataUpdated = Signal(list, list, list) # voltage, current, power

    def __init__(self, select_project_use_case: SelectProject, 
                 configure_power_supply_use_case: ConfigurePowerSupply,
                 add_project_use_case: AddProject,
                 delete_project_use_case: DeleteProject,
                 set_power_supply_voltage_use_case: SetPowerSupplyVoltage,
                 set_power_supply_current_use_case: SetPowerSupplyCurrent,
                 reset_power_supply_settings_use_case: ResetPowerSupplySettings,
                 toggle_power_supply_test_use_case: TogglePowerSupplyTest,
                 parent=None):
        super().__init__(parent)
        self.select_project_use_case = select_project_use_case
        self.configure_power_supply_use_case = configure_power_supply_use_case
        self.add_project_use_case = add_project_use_case
        self.delete_project_use_case = delete_project_use_case
        self.set_power_supply_voltage_use_case = set_power_supply_voltage_use_case
        self.set_power_supply_current_use_case = set_power_supply_current_use_case
        self.reset_power_supply_settings_use_case = reset_power_supply_settings_use_case
        self.toggle_power_supply_test_use_case = toggle_power_supply_test_use_case

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
            print(f"Could not list VISA resources: {e}")
            return []

    @Slot(str, int)
    def setPowerSupplyConfig(self, resource_name, baud_rate):
        if not self._current_project or not self._current_project.power_supply:
            return

        # Use the use case to configure the power supply
        self.configure_power_supply_use_case.execute(
            self._current_project.power_supply, 
            resource_name, 
            baud_rate
        )
        
        self._current_project_proxy.powerSupply.resourceNameChanged.emit()
        self._current_project_proxy.powerSupply.baudRateChanged.emit()

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

    @Slot(str)
    def addProject(self, name):
        if not name:
            return
            
        print(f"Adding project {name} to channel {self._current_channel_index + 1}")
        
        # Use the use case to add a new project
        project = self.add_project_use_case.execute(name, self._current_channel_index)
        
        # Refresh the project list
        self.selectChannel(self._current_channel_index)

    @Slot(int, float)
    def setPowerSupplyVoltage(self, channel_index, voltage):
        if not self._current_project or not self._current_project.power_supply:
            return

        # Use the use case to set the voltage
        self.set_power_supply_voltage_use_case.execute(
            self._current_project.power_supply, 
            channel_index, 
            voltage
        )
        
        # Update UI
        self.currentProjectChanged.emit()

    @Slot(int, float)
    def setPowerSupplyCurrent(self, channel_index, current):
        if not self._current_project or not self._current_project.power_supply:
            return

        # Use the use case to set the current
        self.set_power_supply_current_use_case.execute(
            self._current_project.power_supply, 
            channel_index, 
            current
        )
        
        # Update UI
        self.currentProjectChanged.emit()

    @Slot(bool)
    def togglePowerSupplyTest(self, testing):
        if not self._current_project or not self._current_project.power_supply:
            msg = "没有为测试选择项目."
            print(msg)
            self.powerSupplyTestFailed.emit(msg)
            return

        ps_config = self._current_project.power_supply
        if not ps_config.resource_name:
            msg = "电源资源名称未配置."
            print(msg)
            self.powerSupplyTestFailed.emit(msg)
            return

        # Use the use case to toggle the test
        self.toggle_power_supply_test_use_case.execute(
            ps_config,
            self._current_project,
            testing,
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
            print("No project or power supply selected.")
            return

        print(f"Resetting power supply settings for project {self._current_project.name}")
        
        # Use the use case to reset the settings
        self.reset_power_supply_settings_use_case.execute(self._current_project.power_supply)
        
        # Update UI
        self.currentProjectChanged.emit()

    @Slot()
    def deleteCurrentProject(self):
        if not self._current_project:
            print("No project selected to delete.")
            return

        print(f"Deleting project {self._current_project.name} (ID: {self._current_project.id})")
        
        # Use the use case to delete the project
        self.delete_project_use_case.execute(self._current_project)
        
        # Refresh the project list for the current channel
        self.selectChannel(self._current_channel_index)

    @Slot(int)
    def selectProject(self, index):
        project = self._project_model.get_project(index)
        if project:
            print(f"Project {project.id} selected")
            self._current_project = project
            self._current_project_proxy = ProjectProxy(project)
            self._project_model.set_checked(index)
            self.currentProjectChanged.emit()