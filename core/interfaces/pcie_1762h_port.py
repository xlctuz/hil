from abc import ABC, abstractmethod
from core.entities.pcie_1762h import Pcie1762h


class Pcie1762hPort(ABC):
    """Port interface for PCIE-1762H adapters"""
    
    @abstractmethod
    def run_test(self, pcie_1762h: Pcie1762h):
        """Run a test on the PCIE-1762H device"""
        pass
    
    @abstractmethod
    def get_di(self, pcie_1762h: Pcie1762h) -> int:
        """Get digital input values from the PCIE-1762H device"""
        pass