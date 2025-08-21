from domain.ports.power_supply_polling_service_port import PowerSupplyPollingServicePort
from domain.models.power_supply import PowerSupply
from typing import Callable, Any


class PowerSupplyPollingService(PowerSupplyPollingServicePort):
    def __init__(self):
        # This is a domain service, so it doesn't contain infrastructure-specific code
        # The actual implementation will be in the infrastructure layer
        pass

    def start_polling(self, power_supply: PowerSupply, project: Any, 
                     data_callback: Callable[[dict], None], 
                     error_callback: Callable[[str], None]):
        # This is just a placeholder implementation
        # The actual implementation will be in the infrastructure adapter
        raise NotImplementedError("This method should be implemented in the infrastructure adapter")

    def stop_polling(self):
        # This is just a placeholder implementation
        # The actual implementation will be in the infrastructure adapter
        raise NotImplementedError("This method should be implemented in the infrastructure adapter")