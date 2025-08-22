from core.entities.project import Project
from core.entities.power_supply import PowerSupply
from core.logger import logger
from adapters.devices.power_supply_adapter import PowerSupplyAdapter
from adapters.devices.power_supply_poller import PowerSupplyPoller
from PySide6.QtCore import QThread


class StartPowerSupplyMonitoring:
    def __init__(self, power_supply_adapter: PowerSupplyAdapter):
        self.power_supply_adapter = power_supply_adapter

    def __call__(self, project: Project, data_callback=None, error_callback=None):
        logger.info(f"Starting power supply monitoring for project {project.name} (ID: {project.id})")
        
        if not project.power_supply:
            raise ValueError("Project has no power supply configuration")

        # Create and configure power supply poller
        power_supply = project.power_supply
        poller = PowerSupplyPoller(
            power_supply.resource_name,
            power_supply.baud_rate,
            project
        )

        # Create a thread for the poller
        thread = QThread()
        poller.moveToThread(thread)

        # Connect signals
        if data_callback:
            poller.polledData.connect(data_callback)
        if error_callback:
            poller.error.connect(error_callback)

        # Connect thread signals
        thread.started.connect(poller.start)
        poller.finished.connect(thread.quit)
        poller.finished.connect(poller.deleteLater)
        thread.finished.connect(thread.deleteLater)

        # Start the thread
        thread.start()

        return poller, thread