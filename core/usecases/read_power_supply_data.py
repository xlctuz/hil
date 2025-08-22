from core.entities.project import Project
from core.entities.power_supply import PowerSupply, Channel
from core.logger import logger
from core.interfaces.power_supply_port import PowerSupplyPort
from contextlib import contextmanager


class ReadPowerSupplyData:
    def __init__(self, power_supply_port: PowerSupplyPort):
        self.power_supply_port = power_supply_port

    def __call__(self, project: Project):
        logger.info(f"Reading power supply data for project {project.name} (ID: {project.id})")

        if not project.power_supply:
            raise ValueError("Project has no power supply configuration")

        voltage_data = []
        current_data = []
        power_data = []

        # Create a temporary power supply object for reading data
        power_supply = PowerSupply(project.power_supply.resource_name, project.power_supply.baud_rate)

        try:
            # Open connection
            self.power_supply_port.open(power_supply)

            # Read data for each channel
            # Map channel indices to Channel enum values
            channel_map = {0: Channel.CH1, 1: Channel.CH2, 2: Channel.CH3}

            for channel in project.power_supply.channels:
                try:
                    # Get the corresponding Channel enum value
                    channel_enum = channel_map.get(channel.index, Channel.CH1)

                    # Measure voltage
                    voltage_str = self.power_supply_port.measure_voltage(power_supply, channel_enum)
                    voltage = float(voltage_str.strip())

                    # Measure current
                    current_str = self.power_supply_port.measure_current(power_supply, channel_enum)
                    current = float(current_str.strip())

                    # Calculate power
                    power = voltage * current

                    # Add data to lists
                    voltage_data.append(voltage)
                    current_data.append(current)
                    power_data.append(power)
                except Exception as e:
                    # If there's an error reading a channel, use None values
                    voltage_data.append(None)
                    current_data.append(None)
                    power_data.append(None)
                    logger.info(f"Error reading channel {channel.index}: {str(e)}")
        finally:
            # Close connection
            self.power_supply_port.close(power_supply)

        # Return the data as a dictionary
        return {
            'voltage': voltage_data,
            'current': current_data,
            'power': power_data
        }
