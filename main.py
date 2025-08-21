# main.py
import os
import sys
# import resources_rc
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtQml import QQmlDebuggingEnabler
QQmlDebuggingEnabler.enableDebugging(True)
from PySide6.QtCharts import QChartView, QChart, QLineSeries
import qml.resources_rc
from common.logger import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import core models for database initialization
# We need to import the ORM models from their new location in data_access
# These are used only for database initialization
from data_access.persistence.models.channel import Base as ChannelBase, Channel as ChannelORM
from data_access.persistence.models.project import Base as ProjectBase, Project as ProjectORM
from data_access.persistence.models.power_supply_it6302 import Base as PowerSupplyBase, Power_supply_it6302 as PowerSupplyORM
from data_access.persistence.models.pcie_1762h_controller import Base as Pcie1762hBase, Pcie_1762h as Pcie1762hORM

# Import data access components
from data_access.persistence.database import engine, Session
from data_access.persistence.repositories import ProjectRepository
from data_access.hardware.power_supply_adapter import PowerSupplyAdapter
from data_access.hardware.pcie_1762h_adapter import Pcie1762hAdapter
from data_access.hardware.power_supply_polling_service_adapter import PowerSupplyPollingServiceAdapter

# Import application use cases
from business.application.use_cases.select_project import SelectProject
from business.application.use_cases.configure_power_supply import ConfigurePowerSupply
from business.application.use_cases.add_project import AddProject
from business.application.use_cases.delete_project import DeleteProject
from business.application.use_cases.set_power_supply_voltage import SetPowerSupplyVoltage
from business.application.use_cases.set_power_supply_current import SetPowerSupplyCurrent
from business.application.use_cases.reset_power_supply_settings import ResetPowerSupplySettings
from business.application.use_cases.toggle_power_supply_test import TogglePowerSupplyTest

# Import UI components
from presentation.ui.main_view_model import MainViewModel
from presentation.ui.config_view_model import ConfigViewModel
from presentation.ui.backend_adapter import BackendAdapter


class App:
    def __init__(self):
        # Initialize infrastructure components
        self.project_repository = ProjectRepository()
        self.power_supply_adapter = PowerSupplyAdapter()
        self.pcie_1762h_adapter = Pcie1762hAdapter()
        self.power_supply_polling_service = PowerSupplyPollingServiceAdapter()
        
        # Initialize use cases
        self.select_project_use_case = SelectProject(self.project_repository)
        self.configure_power_supply_use_case = ConfigurePowerSupply(self.power_supply_adapter)
        self.add_project_use_case = AddProject(self.project_repository)
        self.delete_project_use_case = DeleteProject(self.project_repository)
        self.set_power_supply_voltage_use_case = SetPowerSupplyVoltage()
        self.set_power_supply_current_use_case = SetPowerSupplyCurrent()
        self.reset_power_supply_settings_use_case = ResetPowerSupplySettings()
        self.toggle_power_supply_test_use_case = TogglePowerSupplyTest(
            self.power_supply_adapter,
            self.power_supply_polling_service
        )
        
        # Initialize view models
        self._main_view_model = MainViewModel(self.select_project_use_case)
        self._config_view_model = ConfigViewModel(
            self.select_project_use_case,
            self.configure_power_supply_use_case,
            self.add_project_use_case,
            self.delete_project_use_case,
            self.set_power_supply_voltage_use_case,
            self.set_power_supply_current_use_case,
            self.reset_power_supply_settings_use_case,
            self.toggle_power_supply_test_use_case
        )
        
        # Initialize database
        self._initialize_database()

    def _initialize_database(self):
        # Create tables
        ChannelBase.metadata.create_all(engine)
        ProjectBase.metadata.create_all(engine)
        PowerSupplyBase.metadata.create_all(engine)
        Pcie1762hBase.metadata.create_all(engine)
        
        # Create channels if they don't exist
        self.project_repository.create_channels()

    @property
    def mainViewModel(self):
        return self._main_view_model

    @property
    def configViewModel(self):
        return self._config_view_model


if __name__ == "__main__":
    app = QApplication(sys.argv)

    logger.info("main")

    # Create the application components
    app_instance = App()
    
    # Create the QML backend adapter
    backend = BackendAdapter(
        app_instance.mainViewModel,
        app_instance.configViewModel
    )

    appEngine = QQmlApplicationEngine()
    appEngine.addImportPath(os.path.join(os.path.dirname(__file__), "qml/"))

    appEngine.rootContext().setContextProperty("backend", backend)

    appEngine.load(os.path.join(os.path.dirname(__file__), "qml/HILContent/App.qml"))

    if not appEngine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
