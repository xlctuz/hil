from abc import ABC, abstractmethod
from domain.models.pcie_1762h import Pcie1762h, Status


class Pcie1762hPort(ABC):
    @abstractmethod
    def run_test(self, pcie_1762h: Pcie1762h):
        pass

    @abstractmethod
    def get_di(self, pcie_1762h: Pcie1762h):
        pass

    @abstractmethod
    def set_do_channel_name(self, pcie_1762h: Pcie1762h, index: int, name: str):
        pass

    @abstractmethod
    def set_do_channel_status(self, pcie_1762h: Pcie1762h, index: int, status: Status):
        pass