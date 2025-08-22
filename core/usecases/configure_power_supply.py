from core.entities.power_supply import PowerSupply
from core.logger import logger
from core.interfaces.power_supply_port import PowerSupplyPort


class ConfigurePowerSupply:
    def __call__(self, power_supply: PowerSupply, resource_name: str, baud_rate: int):
        logger.info(f"Configuring power supply, resource name {resource_name}, baud_rate {baud_rate}")
        power_supply.resource_name = resource_name
        power_supply.baud_rate = baud_rate