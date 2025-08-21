from business.domain.ports.power_supply_port import PowerSupplyPort
from business.domain.models.power_supply import PowerSupply, IO


class ConfigurePowerSupply:
    def __init__(self, power_supply_port: PowerSupplyPort):
        self.power_supply_port = power_supply_port

    def execute(self, power_supply: PowerSupply, resource_name: str, baud_rate: int):
        power_supply.resource_name = resource_name
        power_supply.baud_rate = baud_rate