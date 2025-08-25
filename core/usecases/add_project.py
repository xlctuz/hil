from typing import List
from core.database import Session
from sqlalchemy import select
from core.logger import logger
from core.entities.project import Project
from core.entities.channel import Channel
from core.entities.pcie_1762h import Pcie1762h
from core.entities.power_supply import PowerSupply
from core.entities.pci1720u import Pci1720u
from core.repositories import ProjectRepository, ChannelRepository


class Add_project:
    def __init__(self, project_repository: ProjectRepository, channel_repository: ChannelRepository):
        self.project_repository = project_repository
        self.channel_repository = channel_repository

    def __call__(self, name: str, channel_index: int) -> Project:

        channel = self.channel_repository.get_by_index(channel_index)
        # Create a new project
        project = Project(name=name)

        # Create default power supply config
        power_supply = PowerSupply(resource_name="ASRL3::INSTR", baud_rate=9600)
        project.power_supply = power_supply

        # Create default PCIE-1762H config
        pcie_1762h = Pcie1762h()
        project.pcie_1762h = pcie_1762h

        # Create default PCI-1720U config
        pci1720u = Pci1720u()
        project.pci1720u = pci1720u

        # Set the channel for the project
        project.channel = channel

        # Save the project
        self.project_repository.save_project(project)

        return project
