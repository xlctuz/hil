from business.domain.models.power_supply import PowerSupply


class SetPowerSupplyCurrent:
    def execute(self, power_supply: PowerSupply, channel_index: int, current: float):
        if 0 <= channel_index < len(power_supply.channels):
            power_supply.channels[channel_index].current = current