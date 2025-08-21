from base.models.power_supply import PowerSupply, IO


class ConfigurePowerSupply:
    def __init__(self):
        pass

    def execute(self, power_supply: PowerSupply, resource_name: str, baud_rate: int):
        power_supply.resource_name = resource_name
        power_supply.baud_rate = baud_rate