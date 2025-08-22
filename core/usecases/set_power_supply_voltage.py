from core.entities.power_supply import PowerSupply
from core.logger import logger


class SetPowerSupplyVoltage:
    def __call__(self, power_supply: PowerSupply, channel_index: int, voltage: float):
        if 0 <= channel_index < len(power_supply.channels):
            power_supply.channels[channel_index].voltage = voltage