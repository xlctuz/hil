from abc import ABC, abstractmethod
from business.domain.models.power_supply import PowerSupply, IO, Channel


class PowerSupplyPort(ABC):
    @abstractmethod
    def open(self, power_supply: PowerSupply):
        pass

    @abstractmethod
    def close(self, power_supply: PowerSupply):
        pass

    @abstractmethod
    def get_idn(self, power_supply: PowerSupply) -> str:
        pass

    @abstractmethod
    def set_voltage(self, power_supply: PowerSupply, channel: int, voltage: float):
        pass

    @abstractmethod
    def get_voltage(self, power_supply: PowerSupply, channel: int) -> float:
        pass

    @abstractmethod
    def set_current(self, power_supply: PowerSupply, channel: int, current: float):
        pass

    @abstractmethod
    def get_current(self, power_supply: PowerSupply, channel: int) -> float:
        pass

    @abstractmethod
    def set_voltage_current(self, power_supply: PowerSupply, channel: Channel, voltage: float, current: float):
        pass

    @abstractmethod
    def measure_current(self, power_supply: PowerSupply, channel: Channel = Channel.ALL) -> str:
        pass

    @abstractmethod
    def measure_voltage(self, power_supply: PowerSupply, channel: Channel = Channel.ALL) -> str:
        pass

    @abstractmethod
    def measure_power(self, power_supply: PowerSupply, channel: Channel = Channel.ALL) -> str:
        pass

    @abstractmethod
    def set_on_off(self, power_supply: PowerSupply, io: IO, channel: Channel = Channel.ALL):
        pass