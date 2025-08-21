from base.models.power_supply import PowerSupply, IO, Channel


class TogglePowerSupplyTest:
    def __init__(self, power_supply_adapter, polling_service):
        self.power_supply_adapter = power_supply_adapter
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