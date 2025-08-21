from domain.models.power_supply import PowerSupply


class SetPowerSupplyVoltage:
    def execute(self, power_supply: PowerSupply, channel_index: int, voltage: float):
        if 0 <= channel_index < len(power_supply.channels):
            power_supply.channels[channel_index].voltage = voltage