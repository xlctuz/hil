from core.entities.project import Project
from core.entities.power_supply import PowerSupply, Channel, IO
from core.interfaces.power_supply_port import PowerSupplyPort
from core.interfaces.pcie_1762h_port import Pcie1762hPort
from core.logger import logger


class StartProject:
    def __init__(self, power_supply_port: PowerSupplyPort, pcie_1762h_port: Pcie1762hPort):
        self.power_supply_port = power_supply_port
        self.pcie_1762h_port = pcie_1762h_port

    def __call__(self, project: Project):
        logger.info(f"Starting project {project.name} (ID: {project.id})")

        # Configure power supply
        if project.power_supply:
            self._configure_power_supply(project.power_supply)

        # Configure DIO
        if project.pcie_1762h:
            self._configure_dio(project.pcie_1762h)

    def _configure_power_supply(self, power_supply_data):
        """Configure the power supply with project settings"""
        try:
            # Create a temporary power supply object for configuration
            temp_power_supply = PowerSupply(power_supply_data.resource_name, power_supply_data.baud_rate)

            # Open connection
            self.power_supply_port.open(temp_power_supply)

            try:
                # Map channel indices to Channel enum values
                channel_map = {0: Channel.CH1, 1: Channel.CH2, 2: Channel.CH3}

                # Configure each channel
                for channel in power_supply_data.channels:
                    if channel.voltage is not None and channel.current is not None:
                        # Get the corresponding Channel enum value
                        channel_enum = channel_map.get(channel.index, Channel.CH1)

                        # Apply voltage and current settings
                        self.power_supply_port.set_voltage_current(
                            temp_power_supply,
                            channel_enum,
                            channel.voltage,
                            channel.current
                        )

                # Turn on power supply
                self.power_supply_port.set_on_off(temp_power_supply, IO.ON)
            finally:
                # Close connection
                self.power_supply_port.close(temp_power_supply)
        except Exception as e:
            raise Exception(f"配置电源失败: {str(e)}")

    def _configure_dio(self, pcie_1762h_data):
        """Configure the DIO with project settings"""
        try:
            # Set DO channels according to project configuration
            self.pcie_1762h_port.run_test(pcie_1762h_data)
        except Exception as e:
            raise Exception(f"配置DIO失败: {str(e)}")
