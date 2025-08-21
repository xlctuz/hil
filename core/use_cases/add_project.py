from base.repositories import ProjectRepository
from base.models.project import Project
from base.models.power_supply import PowerSupply
from base.models.pcie_1762h import Pcie1762h


class AddProject:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def execute(self, name: str, channel_index: int) -> Project:
        # Create a new project
        project = Project(name=name)
        
        # Create default power supply config
        power_supply = PowerSupply(resource_name="ASRL3::INSTR", baud_rate=9600)
        project.power_supply = power_supply
        
        # Create default PCIE-1762H config
        pcie_1762h = Pcie1762h()
        project.pcie_1762h = pcie_1762h
        
        # Set the channel for the project
        from base.models.channel import Channel
        project.channel = Channel(index=channel_index)
        
        # Save the project
        self.project_repository.save_project(project)
        
        return project