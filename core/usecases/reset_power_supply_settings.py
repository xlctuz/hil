from core.entities.power_supply import PowerSupply
from core.logger import logger


class ResetPowerSupplySettings:
    def __call__(self, power_supply: PowerSupply):
        for channel in power_supply.channels:
            channel.voltage = None
            channel.current = None