from core.entities.project import Project
from core.entities.power_supply import PowerSupply
from core.logger import logger
from adapters.devices.power_supply_adapter import PowerSupplyAdapter
from contextlib import contextmanager


class ReadPowerSupplyData:
    def __init__(self, power_supply_adapter: PowerSupplyAdapter):
        self.power_supply_adapter = power_supply_adapter

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
            self.power_supply_adapter.open(power_supply)
            
            # Read data for each channel
            for channel in project.power_supply.channels:
                try:
                    # Measure voltage
                    voltage_str = self.power_supply_adapter.measure_voltage(power_supply, channel)
                    voltage = float(voltage_str.strip())
                    
                    # Measure current
                    current_str = self.power_supply_adapter.measure_current(power_supply, channel)
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
            self.power_supply_adapter.close(power_supply)
        
        # Return the data as a dictionary
        return {
            'voltage': voltage_data,
            'current': current_data,
            'power': power_data
        }