from core.repositories import Repository
from adapters.devices.power_supply_adapter import PowerSupplyAdapter
from .select_project import SelectProject
from .init_channels import Init_channels
from .add_project import Add_project
from .delete_project import Delete_project
from .save_project import SaveProject
from .save_pcie1762h_config import Save_pcie1762h_config
from .configure_power_supply import ConfigurePowerSupply
from .set_power_supply_voltage import SetPowerSupplyVoltage
from .set_power_supply_current import SetPowerSupplyCurrent
from .reset_power_supply_settings import ResetPowerSupplySettings
from .toggle_power_supply_test import TogglePowerSupplyTest
from .start_power_supply_monitoring import StartPowerSupplyMonitoring
from .stop_power_supply_monitoring import StopPowerSupplyMonitoring
from .read_power_supply_data import ReadPowerSupplyData


class UseCases:
    def __init__(self, repository: Repository):
        # Initialize adapters
        self.power_supply_adapter = PowerSupplyAdapter()
        
        # Project management
        self.select_project_from_channel = SelectProject(repository.project)
        self.add_project = Add_project(repository.project, repository.channel)
        self.delete_project = Delete_project(repository.project)
        self.save_project = SaveProject(repository.project)
        
        # Channel initialization
        self.init_channels = Init_channels(repository.channel)
        
        # PCIE-1762H configuration
        self.save_pcie1762h_config = Save_pcie1762h_config(repository.pcie_1762h)
        
        # Power supply configuration
        self.configure_power_supply = ConfigurePowerSupply()
        self.set_power_supply_voltage = SetPowerSupplyVoltage()
        self.set_power_supply_current = SetPowerSupplyCurrent()
        self.reset_power_supply_settings = ResetPowerSupplySettings()
        self.toggle_power_supply_test = TogglePowerSupplyTest()
        
        # Power supply monitoring
        self.start_power_supply_monitoring = StartPowerSupplyMonitoring(self.power_supply_adapter)
        self.stop_power_supply_monitoring = StopPowerSupplyMonitoring()
        self.read_power_supply_data = ReadPowerSupplyData(self.power_supply_adapter)