from core.entities.project import Project
from core.logger import logger
from typing import Callable
from core.interfaces.scheduler_port import SchedulerPort
from .read_pcie_1762h_data import ReadPcie1762hData


class StartPcie1762hMonitoring:
    def __init__(self, scheduler_factory: Callable[[], SchedulerPort], read_pcie_1762h_data_usecase: ReadPcie1762hData):
        self.scheduler_factory = scheduler_factory
        self.read_pcie_1762h_data_usecase = read_pcie_1762h_data_usecase

    def __call__(self, project: Project, data_callback=None, error_callback=None):
        logger.info(f"Starting PCIE-1762H monitoring for project {project.name} (ID: {project.id})")
        
        if not project.pcie_1762h:
            raise ValueError("Project has no PCIE-1762H configuration")

        def poll_data():
            try:
                data = self.read_pcie_1762h_data_usecase(project.pcie_1762h)
                if data_callback:
                    data_callback(data)
            except Exception as e:
                if error_callback:
                    error_callback(f"Error polling DIO data: {str(e)}")

        # Create a new scheduler instance
        scheduler = self.scheduler_factory()

        # Start the scheduler with a 0.5-second interval
        scheduler.start_polling(0.5, poll_data)

        return scheduler
