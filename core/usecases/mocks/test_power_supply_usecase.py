import sys
import os
from PySide6.QtCore import QCoreApplication, QObject

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir)))

from core.entities.project import Project
from core.entities.power_supply import PowerSupply, PowerSupplyChannel
from core.repositories import Repository
from core.usecases import UseCases
from core.usecases.mocks.mock_power_supply_adapter import MockPowerSupplyAdapter
from core.usecases.mocks.mock_scheduler_adapter import MockSchedulerAdapter


class TestPowerSupplyUsecase(QObject):
    """Test class for power supply use cases with mock adapter"""
    
    def __init__(self):
        super().__init__()
        self.app = QCoreApplication(sys.argv)
        
        # Create mock adapters
        self.mock_power_supply_adapter = MockPowerSupplyAdapter()
        self.mock_scheduler_adapter = MockSchedulerAdapter()
        
        # Create a repository and use cases with the mock adapters
        self.repository = Repository()
        self.usecases = UseCases(self.repository, self.mock_power_supply_adapter, self.mock_scheduler_adapter)
        
        # Create a test project with power supply configuration
        self.project = self._create_test_project()
        
        # Variables to store scheduler
        self.scheduler = None
        
    def _create_test_project(self):
        """Create a test project with power supply configuration"""
        project = Project(name="Test Project")
        
        # Create power supply configuration
        power_supply = PowerSupply(resource_name="MOCK::RESOURCE", baud_rate=9600)
        
        # Add channels to the power supply
        for i in range(3):
            channel = PowerSupplyChannel()
            channel.index = i
            power_supply.channels.append(channel)
        
        # Configure channels with some test values
        power_supply.channels[0].voltage = 5.0
        power_supply.channels[0].current = 1.0
        power_supply.channels[1].voltage = 12.0
        power_supply.channels[1].current = 0.5
        power_supply.channels[2].voltage = 3.3
        power_supply.channels[2].current = 2.0
        
        project.power_supply = power_supply
        
        return project
    
    def on_data_received(self, data):
        """Handle received power supply data"""
        print(f"Received data: {data}")
        
        # Check if we have received data for all channels
        voltage_data = data.get('voltage', [])
        current_data = data.get('current', [])
        power_data = data.get('power', [])
        
        if len(voltage_data) >= 3 and len(current_data) >= 3 and len(power_data) >= 3:
            print("Received data for all channels:")
            for i in range(3):
                v = voltage_data[i] if voltage_data[i] is not None else 0.0
                c = current_data[i] if current_data[i] is not None else 0.0
                p = power_data[i] if power_data[i] is not None else 0.0
                print(f"  Channel {i+1}: V={v:.2f}, I={c:.2f}, P={p:.2f}")
        
        # After receiving 5 data points, stop monitoring
        if not hasattr(self, '_data_count'):
            self._data_count = 0
        self._data_count += 1
        
        if self._data_count >= 5:
            print("Received 5 data points, stopping monitoring...")
            self.stop_monitoring()
    
    def on_error(self, error_message):
        """Handle error messages"""
        print(f"Error: {error_message}")
        self.stop_monitoring()
    
    def test_read_power_supply_data(self):
        """Test reading power supply data"""
        print("Testing read power supply data use case...")
        
        try:
            # Configure the power supply first
            from core.entities.power_supply import Channel, IO
            self.usecases.configure_power_supply(self.project.power_supply, "MOCK::RESOURCE", 9600)
            self.usecases.set_power_supply_voltage(self.project.power_supply, 0, 5.0)
            self.usecases.set_power_supply_current(self.project.power_supply, 0, 1.0)
            self.usecases.set_power_supply_voltage(self.project.power_supply, 1, 12.0)
            self.usecases.set_power_supply_current(self.project.power_supply, 1, 0.5)
            self.usecases.set_power_supply_voltage(self.project.power_supply, 2, 3.3)
            self.usecases.set_power_supply_current(self.project.power_supply, 2, 2.0)
            
            # Turn on the power supply to get non-zero readings
            # We need to open the connection first
            self.mock_power_supply_adapter.open(self.project.power_supply)
            self.mock_power_supply_adapter.set_voltage_current(self.project.power_supply, Channel.CH1, 5.0, 1.0)
            self.mock_power_supply_adapter.set_voltage_current(self.project.power_supply, Channel.CH2, 12.0, 0.5)
            self.mock_power_supply_adapter.set_voltage_current(self.project.power_supply, Channel.CH3, 3.3, 2.0)
            self.mock_power_supply_adapter.set_on_off(self.project.power_supply, IO.ON)
            
            # Read the data
            data = self.usecases.read_power_supply_data(self.project)
            print(f"Read data: {data}")
            
        except Exception as e:
            print(f"Error reading power supply data: {e}")
        finally:
            self.app.quit()
    
    def test_start_stop_monitoring(self):
        """Test starting and stopping power supply monitoring"""
        print("Testing start/stop power supply monitoring use case...")
        
        try:
            # Configure the power supply first
            self.usecases.configure_power_supply(self.project.power_supply, "MOCK::RESOURCE", 9600)
            self.usecases.set_power_supply_voltage(self.project.power_supply, 0, 5.0)
            self.usecases.set_power_supply_current(self.project.power_supply, 0, 1.0)
            self.usecases.set_power_supply_voltage(self.project.power_supply, 1, 12.0)
            self.usecases.set_power_supply_current(self.project.power_supply, 1, 0.5)
            self.usecases.set_power_supply_voltage(self.project.power_supply, 2, 3.3)
            self.usecases.set_power_supply_current(self.project.power_supply, 2, 2.0)
            
            # Turn on the power supply
            self.mock_power_supply_adapter.open(self.project.power_supply)
            from core.entities.power_supply import IO
            self.mock_power_supply_adapter.set_on_off(self.project.power_supply, IO.ON)
            
            # Start monitoring
            self.scheduler = self.usecases.start_power_supply_monitoring(
                self.project,
                self.on_data_received,
                self.on_error
            )
            
            print("Monitoring started, waiting for data...")
            
        except Exception as e:
            print(f"Error starting power supply monitoring: {e}")
            self.app.quit()
    
    def stop_monitoring(self):
        """Stop power supply monitoring"""
        print("Stopping power supply monitoring...")
        
        try:
            # Use the use case to stop monitoring
            self.usecases.stop_power_supply_monitoring(self.scheduler)
        except Exception as e:
            print(f"Error stopping monitoring: {e}")
        finally:
            # Quit the application
            self.app.quit()
    
    def run(self, test_type="monitoring"):
        """Run the test"""
        print("Power Supply Usecase Test")
        print("=========================")
        
        if test_type == "read":
            # Test reading data
            self.test_read_power_supply_data()
        else:
            # Test monitoring
            self.test_start_stop_monitoring()
        
        # Run the Qt event loop
        return self.app.exec


if __name__ == "__main__":
    test_type = "read" if len(sys.argv) > 1 and sys.argv[1] == "read" else "monitoring"
    test = TestPowerSupplyUsecase()
    sys.exit(test.run(test_type))