from abc import ABC, abstractmethod
from domain.models.power_supply import PowerSupply
from typing import Callable, Any


class PowerSupplyPollingServicePort(ABC):
    @abstractmethod
    def start_polling(self, power_supply: PowerSupply, project: Any, 
                     data_callback: Callable[[dict], None], 
                     error_callback: Callable[[str], None]):
        pass

    @abstractmethod
    def stop_polling(self):
        pass