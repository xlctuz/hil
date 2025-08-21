from domain.models.power_supply import PowerSupply


class ResetPowerSupplySettings:
    def execute(self, power_supply: PowerSupply):
        for channel in power_supply.channels:
            channel.voltage = None
            channel.current = None