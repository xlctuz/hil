from core.interfaces.pcie_1762h_port import Pcie1762hPort
from core.entities.pcie_1762h import Pcie1762h, Status
import random


class MockPcie1762hAdapter(Pcie1762hPort):
    """Mock adapter for PCIE-1762H testing"""

    def __init__(self):
        # Initialize with default values
        self._do_channels = [Status.LOW] * 16
        self._di_channels = [Status.LOW] * 16

        # Randomly set some initial DI channels to HIGH for testing
        for i in range(16):
            if random.choice([True, False]):
                self._di_channels[i] = Status.HIGH

    def run_test(self, pcie_1762h: Pcie1762h):
        """Run a test on the PCIE-1762H device (mock implementation)"""
        # Update the internal DO channel states based on the pcie_1762h configuration
        for channel in pcie_1762h.do_channels:
            if 0 <= channel.index < 16:
                self._do_channels[channel.index] = channel.status

        # For demo purposes, we'll also update some DI channels based on DO channels
        # In a real implementation, DI channels would be controlled by external factors
        for i in range(16):
            # If DO channel is HIGH, there's a 90% chance the corresponding DI channel is HIGH
            # If DO channel is LOW, there's a 10% chance the corresponding DI channel is HIGH
            if self._do_channels[i] == Status.HIGH:
                self._di_channels[i] = Status.HIGH if random.random() < 0.9 else Status.LOW
            else:
                self._di_channels[i] = Status.HIGH if random.random() < 0.1 else Status.LOW

    def get_di(self, pcie_1762h: Pcie1762h) -> int:
        """Get digital input values from the PCIE-1762H device (mock implementation)"""
        # Convert the DI channel states to an integer value
        data = 0
        for i in range(16):
            if self._di_channels[i] == Status.HIGH:
                data |= (1 << i)

        return data
