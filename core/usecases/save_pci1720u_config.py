from core.repositories import Repository
from core.entities.pci1720u import Pci1720u
from core.logger import logger


class SavePci1720uConfig:
    def __init__(self, repository: Repository):
        self.repository = repository

    def __call__(self, data: Pci1720u):
        # The project object is managed by SQLAlchemy's session,
        # so we just need to save the whole project.

        logger.info(f"save {data}, channel 0 name {data.channels[0].name}")
        self.repository.save(data)
