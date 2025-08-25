from core.entities.project import Project
from core.entities.power_supply import PowerSupply, IO
from core.interfaces.power_supply_port import PowerSupplyPort
from core.logger import logger


class StopProject:
    def __init__(self, power_supply_port: PowerSupplyPort):
        self.power_supply_port = power_supply_port

    def __call__(self, project: Project):
        logger.info(f"Stopping project {project.name} (ID: {project.id})")

        if project.power_supply:
            self._turn_off_power_supply(project.power_supply)

    def _turn_off_power_supply(self, power_supply_data):
        """Turn off the power supply"""
        try:
            # Create a temporary power supply object for configuration
            temp_power_supply = PowerSupply(power_supply_data.resource_name, power_supply_data.baud_rate)

            # Open connection
            self.power_supply_port.open(temp_power_supply)

            try:
                # Turn off power supply
                self.power_supply_port.set_on_off(temp_power_supply, IO.OFF)
            finally:
                # Close connection
                self.power_supply_port.close(temp_power_supply)
        except Exception as e:
            logger.error(f"Error turning off power supply: {str(e)}")
