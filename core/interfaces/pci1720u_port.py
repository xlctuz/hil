from abc import ABC, abstractmethod
from core.entities.pci1720u import Pci1720u


class Pci1720uPort(ABC):
    """Port interface for PCI-1720U adapters"""

    @abstractmethod
    def set_voltage(self, pci1720u: Pci1720u, channel_index: int, voltage: float):
        """Set the output voltage for a specific channel."""
        pass

    @abstractmethod
    def get_device_description(self, device_number: int) -> str:
        """Get the description of the device."""
        pass
