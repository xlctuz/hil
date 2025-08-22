from abc import ABC, abstractmethod
from core.entities.power_supply import PowerSupply, IO, Channel


class PowerSupplyPort(ABC):
    """Port interface for power supply adapters"""
    
    @abstractmethod
    def open(self, power_supply: PowerSupply):
        """Open connection to the power supply"""
        pass
    
    @abstractmethod
    def close(self, power_supply: PowerSupply):
        """Close connection to the power supply"""
        pass
    
    @abstractmethod
    def set_voltage(self, power_supply: PowerSupply, channel: int, voltage: float):
        """Set voltage for a channel"""
        pass
    
    @abstractmethod
    def get_voltage(self, power_supply: PowerSupply, channel: int) -> float:
        """Get voltage for a channel"""
        pass
    
    @abstractmethod
    def set_current(self, power_supply: PowerSupply, channel: int, current: float):
        """Set current for a channel"""
        pass
    
    @abstractmethod
    def get_current(self, power_supply: PowerSupply, channel: int) -> float:
        """Get current for a channel"""
        pass
    
    @abstractmethod
    def set_voltage_current(self, power_supply: PowerSupply, channel: Channel, voltage: float, current: float):
        """Set both voltage and current for a channel"""
        pass
    
    @abstractmethod
    def measure_current(self, power_supply: PowerSupply, channel: Channel = Channel.ALL) -> str:
        """Measure current for a channel"""
        pass
    
    @abstractmethod
    def measure_voltage(self, power_supply: PowerSupply, channel: Channel = Channel.ALL) -> str:
        """Measure voltage for a channel"""
        pass
    
    @abstractmethod
    def measure_power(self, power_supply: PowerSupply, channel: Channel = Channel.ALL) -> str:
        """Measure power for a channel"""
        pass
    
    @abstractmethod
    def set_on_off(self, power_supply: PowerSupply, io: IO, channel: Channel = Channel.ALL):
        """Turn output on or off"""
        pass