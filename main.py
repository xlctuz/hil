# main.py
import os
import sys
# import resources_rc
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

from core.repositories import Repository
from core.usecases import UseCases

from adapters.devices.power_supply_adapter import PowerSupplyAdapter
from adapters.devices.pcie_1762h_adapter import Pcie1762hAdapter
from adapters.devices.power_supply_polling_service_adapter import PowerSupplyPollingServiceAdapter
from adapters.views.main.main_view_model import MainViewModel
from adapters.views.config.config_view_model import ConfigViewModel
from adapters.views.backend_adapter import BackendAdapter

from core.usecases.mocks.mock_power_supply_adapter import MockPowerSupplyAdapter

# class App:
#     def __init__(self):
#         # Initialize infrastructure components
#         self.power_supply_adapter = PowerSupplyAdapter()
#         self.pcie_1762h_adapter = Pcie1762hAdapter()
#         self.power_supply_polling_service = PowerSupplyPollingServiceAdapter()

#         self.repository = Repository()
#         self.usecases = UseCases(self.repository)

#         # Initialize view models
#         self._main_view_model = MainViewModel(self.usecases)
#         self._config_view_model = ConfigViewModel(
#             self.usecases,
#             self.power_supply_adapter,
#             self.power_supply_polling_service
#         )

#         # Initialize database
#         self._initialize_database()

#     def _initialize_database(self):
#         # Create tables
#         Base.metadata.create_all(engine)

#         self.usecases.init_channels()




#     @property
#     def mainViewModel(self):
#         return self._main_view_model

#     @property
#     def configViewModel(self):
#         return self._config_view_model


from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.repositories import Repository
from core.usecases import UseCases
from adapters.views.backend_adapter import BackendAdapter
from adapters.views.main.main_view_model import MainViewModel
from adapters.views.config.config_view_model import ConfigViewModel
from adapters.devices.power_supply_adapter import PowerSupplyAdapter
from adapters.schedulers.qt_scheduler_adapter import QtSchedulerAdapter
from core.usecases.mocks.mock_power_supply_adapter import MockPowerSupplyAdapter

if __name__ == "__main__":
    # Create QML application
    app = QApplication(sys.argv)

    # Create core components
    repository = Repository()
    if 0:
        power_supply_adapter = PowerSupplyAdapter()
    else:
        power_supply_adapter = MockPowerSupplyAdapter()
    scheduler_adapter = QtSchedulerAdapter()
    use_cases = UseCases(repository, power_supply_adapter, scheduler_adapter)

    # Initialize channels if needed
    use_cases.init_channels()

    # Create view models
    main_view_model = MainViewModel(use_cases)
    config_view_model = ConfigViewModel(use_cases, power_supply_adapter, scheduler_adapter)

    # Create backend adapter
    backend_adapter = BackendAdapter(main_view_model, config_view_model)

    # Create QML engine and set context properties
    engine = QQmlApplicationEngine()
    engine.addImportPath(os.path.join(os.path.dirname(__file__), "qml/"))
    engine.rootContext().setContextProperty("backend", backend_adapter)
    engine.load(os.path.join(os.path.dirname(__file__), "qml/HILContent/App.qml"))

    # Load the main QML file
    qml_file = os.path.join(os.path.dirname(__file__), "qml", "main.qml")
    engine.load(qml_file)

    # Check if the QML file was loaded successfully
    if not engine.rootObjects():
        sys.exit(-1)

    # Run the application
    sys.exit(app.exec())
