import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir)))

from core.entities.pcie_1762h import Pcie1762h, Pcie1762hDoChannel, Pcie1762hDiChannel, Status
from core.repositories import Repository
from core.usecases import UseCases
from core.usecases.mocks.mock_pcie_1762h_adapter import MockPcie1762hAdapter
from core.usecases.mocks.mock_power_supply_adapter import MockPowerSupplyAdapter
from core.usecases.mocks.mock_scheduler_adapter import MockSchedulerAdapter


class TestPcie1762hUsecase:
    """Test class for PCIE-1762H use case with mock adapter"""
    
    def __init__(self):
        # Create mock adapters
        self.mock_power_supply_adapter = MockPowerSupplyAdapter()
        self.mock_pcie_1762h_adapter = MockPcie1762hAdapter()
        self.mock_scheduler_adapter = MockSchedulerAdapter()
        
        # Create a repository and use cases with the mock adapters
        self.repository = Repository()
        self.usecases = UseCases(
            self.repository, 
            self.mock_power_supply_adapter, 
            self.mock_scheduler_adapter,
            self.mock_pcie_1762h_adapter
        )
        
        # Create a test PCIE-1762H configuration
        self.pcie_1762h = self._create_test_pcie_1762h()
        
    def _create_test_pcie_1762h(self):
        """Create a test PCIE-1762H configuration"""
        pcie_1762h = Pcie1762h()
        
        # Configure some DO channels to HIGH for testing
        for i in range(16):
            channel = Pcie1762hDoChannel()
            channel.index = i
            channel.name = f"DO Channel {i}"
            # Set even channels to HIGH, odd channels to LOW
            channel.status = Status.HIGH if i % 2 == 0 else Status.LOW
            pcie_1762h.do_channels.append(channel)
            
        # Add DI channels
        for i in range(16):
            channel = Pcie1762hDiChannel()
            channel.index = i
            channel.name = f"DI Channel {i}"
            pcie_1762h.di_channels.append(channel)
            
        return pcie_1762h
    
    def test_pcie_1762h(self):
        """Test the PCIE-1762H use case"""
        print("Testing PCIE-1762H use case...")
        
        try:
            # Run the test use case
            di_data = self.usecases.test_pcie_1762h(self.pcie_1762h)
            
            # Print the results
            print(f"DI data: {di_data} (0x{di_data:04X})")
            
            # Print individual channel states
            print("DI Channel States:")
            for i in range(16):
                state = "HIGH" if (di_data >> i) & 1 else "LOW"
                print(f"  Channel {i}: {state}")
                
        except Exception as e:
            print(f"Error testing PCIE-1762H: {e}")


if __name__ == "__main__":
    test = TestPcie1762hUsecase()
    test.test_pcie_1762h()