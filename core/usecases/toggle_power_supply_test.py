from core.entities.power_supply import PowerSupply
from core.logger import logger


class TogglePowerSupplyTest:
    def __call__(self, power_supply: PowerSupply, project: object, testing: bool,
                 power_supply_adapter, polling_service, data_callback=None, error_callback=None):
        if testing:
            # Start polling using the polling service
            polling_service.start_polling(
                power_supply,
                project,
                data_callback,
                error_callback
            )
        else:
            # Stop polling
            polling_service.stop_polling()