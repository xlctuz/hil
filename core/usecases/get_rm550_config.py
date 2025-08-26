from core.repositories import Repository
from core.entities.rm550 import RM550

class GetRM550ConfigUseCase:
    def __init__(self, repository: Repository):
        self.repository = repository

    def execute(self) -> RM550:
        return self.repository.rm550.get_rm550_config()
