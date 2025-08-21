from business.domain.models.channel import Channel
from business.domain.models.power_supply import PowerSupply
from business.domain.models.pcie_1762h import Pcie1762h


class Project:
    def __init__(self, name=""):
        self.id = None
        self.name = name
        self.channel = None  # type: Channel
        self.power_supply = None  # type: PowerSupply
        self.pcie_1762h = None  # type: Pcie1762h