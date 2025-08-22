from core.entities.power_supply import PowerSupply
from adapters.devices.power_supply_poller import PowerSupplyPoller
from PySide6.QtCore import QThread
from typing import Callable, Any


class PowerSupplyPollingServiceAdapter:
    def __init__(self):
        self._poller_thread = None
        self._poller = None

    def start_polling(self, power_supply: PowerSupply, project: Any, 
                     data_callback: Callable[[dict], None], 
                     error_callback: Callable[[str], None]):
        # Stop any existing poller first
        if self._poller_thread and self._poller_thread.isRunning():
            self._poller.stop()
            self._poller_thread.quit()
            self._poller_thread.wait()

        # Setup and start the poller thread
        self._poller_thread = QThread()
        self._poller = PowerSupplyPoller(
            power_supply.resource_name, 
            power_supply.baud_rate, 
            project
        )
        
        # Connect signals
        if data_callback:
            self._poller.polledData.connect(data_callback)
        if error_callback:
            self._poller.error.connect(error_callback)
            
        self._poller.moveToThread(self._poller_thread)
        self._poller_thread.started.connect(self._poller.start)
        self._poller.finished.connect(self._poller_thread.quit)
        self._poller_thread.start()

    def stop_polling(self):
        if self._poller:
            self._poller.stop()
        if self._poller_thread:
            self._poller_thread.quit()
            self._poller_thread.wait()
            self._poller_thread = None
            self._poller = None