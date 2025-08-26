from core.interfaces.pci1720u_port import Pci1720uPort
from core.entities.pci1720u import Pci1720u
from core.logger import logger

class MockPci1720uAdapter(Pci1720uPort):
    """Mock adapter for PCI-1720U testing"""

    def __init__(self):
        self.voltages = {} # Store voltages per device_number and channel
        logger.info("Initialized MockPci1720uAdapter")

    def set_voltage(self, pci1720u: Pci1720u, channel_index: int, voltage: float):
        device_key = pci1720u.device_number
        if device_key not in self.voltages:
            self.voltages[device_key] = {}

        self.voltages[device_key][channel_index] = voltage
        logger.info(f"[Mock] Set PCI-1720U Device#{device_key} Channel {channel_index} to {voltage}V")

    def get_device_description(self, device_number: int) -> str:
        return f"MockPCI-1720U,BID#{device_number}"
