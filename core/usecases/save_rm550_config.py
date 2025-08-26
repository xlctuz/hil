from core.repositories import Repository
from core.entities.rm550 import RM550

class SaveRM550ConfigUseCase:
    def __init__(self, repository: Repository):
        self.repository = repository

    def execute(self, config: RM550):
        self.repository.rm550.save_rm550_config(config)
