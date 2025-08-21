from business.domain.ports.power_supply_port import PowerSupplyPort
from business.domain.ports.power_supply_polling_service_port import PowerSupplyPollingServicePort
from business.domain.models.power_supply import PowerSupply, IO, Channel


class TogglePowerSupplyTest:
    def __init__(self, power_supply_port: PowerSupplyPort, polling_service: PowerSupplyPollingServicePort):
        self.power_supply_port = power_supply_port
        self.polling_service = polling_service

    def execute(self, power_supply: PowerSupply, project: object, testing: bool, data_callback=None, error_callback=None):
        if testing:
            # Start polling using the polling service
            self.polling_service.start_polling(
                power_supply, 
                project, 
                data_callback, 
                error_callback
            )
        else:
            # Stop polling
            self.polling_service.stop_polling()