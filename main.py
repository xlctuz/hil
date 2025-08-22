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
from core.logger import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import core models for database initialization
# We need to import the ORM models from their new location in base
# These are used only for database initialization
from core.entities.channel import Channel
from core.entities.project import Project
from core.entities.power_supply import PowerSupply
from core.entities.pcie_1762h import Pcie1762h
from core.database import Base

from core.database import engine, Session
from core.repositories import Repository
from core.usecases import UseCases

from adapters.devices.power_supply_adapter import PowerSupplyAdapter
from adapters.devices.pcie_1762h_adapter import Pcie1762hAdapter
from adapters.devices.power_supply_polling_service_adapter import PowerSupplyPollingServiceAdapter
from adapters.views.main.main_view_model import MainViewModel
from adapters.views.config.config_view_model import ConfigViewModel
from adapters.views.backend_adapter import BackendAdapter


class App:
    def __init__(self):
        # Initialize infrastructure components
        self.power_supply_adapter = PowerSupplyAdapter()
        self.pcie_1762h_adapter = Pcie1762hAdapter()
        self.power_supply_polling_service = PowerSupplyPollingServiceAdapter()

        self.repository = Repository()
        self.usecases = UseCases(self.repository)

        # Initialize view models
        self._main_view_model = MainViewModel(self.usecases)
        self._config_view_model = ConfigViewModel(
            self.usecases,
            self.power_supply_adapter,
            self.power_supply_polling_service
        )

        # Initialize database
        self._initialize_database()

    def _initialize_database(self):
        # Create tables
        Base.metadata.create_all(engine)

        self.usecases.init_channels()




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
