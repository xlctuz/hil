from core.entities.pcie_1762h import Pcie1762h, Pcie1762hDoChannel, Pcie1762hDiChannel, Status
from core.usecases.mocks.mock_pcie_1762h_adapter import MockPcie1762hAdapter


class TestPcie1762h:
    def __init__(self, pcie_1762h_port):
        self.pcie_1762h_port = pcie_1762h_port

    def __call__(self, pcie_1762h: Pcie1762h):
        """Test the PCIE-1762H device"""
        # Run the test using the port
        self.pcie_1762h_port.run_test(pcie_1762h)
        
        # Get digital input values
        di_data = self.pcie_1762h_port.get_di(pcie_1762h)
        
        # Return the DI data
        return di_data