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
# We need to import the ORM models from their new location in base
# These are used only for database initialization
from base.models.channel import Base as ChannelBase, Channel
from base.models.project import Base as ProjectBase, ProjectORM
from base.models.power_supply import Base as PowerSupplyBase, PowerSupply
from base.models.pcie_1762h import Base as Pcie1762hBase, Pcie1762h

# Import base components
from base.database import engine, Session
from base.repositories import ProjectRepository
from base.devices.power_supply_adapter import PowerSupplyAdapter
from base.devices.pcie_1762h_adapter import Pcie1762hAdapter
from base.devices.power_supply_polling_service_adapter import PowerSupplyPollingServiceAdapter

# Import core use cases
from core.use_cases.project_management import ProjectManagement
from core.use_cases.power_supply_management import PowerSupplyConfiguration

# Import UI components
from ui.main_view_model import MainViewModel
from ui.config_view_model import ConfigViewModel
from ui.backend_adapter import BackendAdapter


class App:
    def __init__(self):
        # Initialize infrastructure components
        self.project_repository = ProjectRepository()
        self.power_supply_adapter = PowerSupplyAdapter()
        self.pcie_1762h_adapter = Pcie1762hAdapter()
        self.power_supply_polling_service = PowerSupplyPollingServiceAdapter()
        
        # Initialize use cases
        self.project_management_use_case = ProjectManagement(self.project_repository)
        self.power_supply_configuration_use_case = PowerSupplyConfiguration()
        
        # Initialize view models
        self._main_view_model = MainViewModel(self.project_management_use_case)
        self._config_view_model = ConfigViewModel(
            self.project_management_use_case,
            self.power_supply_configuration_use_case,
            self.power_supply_adapter,
            self.power_supply_polling_service
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
