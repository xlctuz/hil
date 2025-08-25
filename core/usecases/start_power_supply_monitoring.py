from core.entities.project import Project
from core.logger import logger
from core.interfaces.power_supply_port import PowerSupplyPort
from typing import Callable
from core.interfaces.scheduler_port import SchedulerPort


class StartPowerSupplyMonitoring:
    def __init__(self, power_supply_port: PowerSupplyPort, scheduler_factory: Callable[[], SchedulerPort], read_power_supply_data_usecase):
        self.power_supply_port = power_supply_port
        self.scheduler_factory = scheduler_factory
        self.read_power_supply_data_usecase = read_power_supply_data_usecase

    def __call__(self, project: Project, data_callback=None, error_callback=None):
        logger.info(f"Starting power supply monitoring for project {project.name} (ID: {project.id})")
        
        if not project.power_supply:
            raise ValueError("Project has no power supply configuration")

        # Define the polling function
        def poll_data():
            try:
                # Read power supply data using the use case
                data = self.read_power_supply_data_usecase(project)
                
                # Call the data callback with the read data
                if data_callback:
                    data_callback(data)
            except Exception as e:
                # Call the error callback if an exception occurs
                if error_callback:
                    error_callback(f"Error polling power supply: {str(e)}")

        # Create a new scheduler instance
        scheduler = self.scheduler_factory()
        
        # Start the scheduler with a 1-second interval
        scheduler.start_polling(1.0, poll_data)

        # Return the new scheduler instance so it can be stopped later
        return scheduler