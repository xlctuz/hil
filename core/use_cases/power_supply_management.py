from base.models.power_supply import PowerSupply, IO, Channel
from base.logger import logger


class PowerSupplyConfiguration:
    def __init__(self):
        pass

    def configure_power_supply(self, power_supply: PowerSupply, resource_name: str, baud_rate: int):
        logger.info(f"config power supply, resource name {resource_name}, baud_rate {baud_rate}")
        power_supply.resource_name = resource_name
        power_supply.baud_rate = baud_rate

    def set_power_supply_voltage(self, power_supply: PowerSupply, channel_index: int, voltage: float):
        if 0 <= channel_index < len(power_supply.channels):
            power_supply.channels[channel_index].voltage = voltage

    def set_power_supply_current(self, power_supply: PowerSupply, channel_index: int, current: float):
        if 0 <= channel_index < len(power_supply.channels):
            power_supply.channels[channel_index].current = current

    def reset_power_supply_settings(self, power_supply: PowerSupply):
        for channel in power_supply.channels:
            channel.voltage = None
            channel.current = None

    def toggle_power_supply_test(self, power_supply: PowerSupply, project: object, testing: bool,
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


power_supply_config = PowerSupplyConfiguration()
