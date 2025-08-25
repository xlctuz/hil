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
from adapters.devices.pcie_1762h_adapter import Pcie1762hAdapter
from adapters.schedulers.qt_scheduler_adapter import QtSchedulerAdapter
from core.usecases.mocks.mock_power_supply_adapter import MockPowerSupplyAdapter
from core.usecases.mocks.mock_pcie_1762h_adapter import MockPcie1762hAdapter

if __name__ == "__main__":
    # Create QML application
    app = QApplication(sys.argv)

    # Create core components
    repository = Repository()
    if 0:
        power_supply_adapter = PowerSupplyAdapter()
        pcie_1762h_adapter = Pcie1762hAdapter()
    else:
        power_supply_adapter = MockPowerSupplyAdapter()
        pcie_1762h_adapter = MockPcie1762hAdapter()
    scheduler_factory = lambda: QtSchedulerAdapter()
    use_cases = UseCases(repository, power_supply_adapter, scheduler_factory, pcie_1762h_adapter)

    # Initialize channels if needed
    use_cases.init_channels()

    # Create view models
    main_view_model = MainViewModel(use_cases)
    config_view_model = ConfigViewModel(use_cases, power_supply_adapter)

    # Create backend adapter
    backend_adapter = BackendAdapter(main_view_model, config_view_model)

    # Create QML engine and set context properties
    engine = QQmlApplicationEngine()
    engine.addImportPath(os.path.join(os.path.dirname(__file__), "qml/"))
    engine.rootContext().setContextProperty("backend", backend_adapter)
    engine.load(os.path.join(os.path.dirname(__file__), "qml/HILContent/App.qml"))

    # Check if the QML file was loaded successfully
    if not engine.rootObjects():
        sys.exit(-1)

    # Run the application
    sys.exit(app.exec())
