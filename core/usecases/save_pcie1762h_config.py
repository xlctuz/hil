from core.repositories import Pcie1762hRepository

class Save_pcie1762h_config:
    def __init__(self, repository: Pcie1762hRepository):
        self.repo = repository

    def __call__(self, data):
        self.repo.save(data)
