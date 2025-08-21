from base.models.pcie_1762h import Pcie1762h
from base.repositories import repository
from base.logger import logger


class Pcie1726hConfig:
    def save(self, data):
        repository.pcie_1762h.save(data)



pcie1726h_config = Pcie1726hConfig()
