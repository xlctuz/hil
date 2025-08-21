from .power_supply_management import power_supply_config
from .project_management import project_management
from .pcie_1726_config import pcie1726h_config


class UseCases:
    def __init__(self):
        self.project_management = project_management
        self.power_supply_config = power_supply_config
        self.pcie1726h_config = pcie1726h_config


use_cases = UseCases()
