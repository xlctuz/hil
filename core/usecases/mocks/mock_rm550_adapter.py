from core.interfaces.rm550_port import RM550Port
from core.logger import logger
import time
import random

class MockRM550Adapter(RM550Port):
    """Mock adapter for the RM550 device for testing purposes."""

    def __init__(self):
        self._connected = False
        self._resistance = 100.0
        self._is_enabled = False
        logger.info("Initialized MockRM550Adapter")

    def connect(self, port: str, baudrate: int) -> bool:
        """Simulates connecting to the RM550 device."""
        logger.info(f"MockRM550: Attempting to connect to {port} at {baudrate} baud.")
        if "COM" in port:
            self._connected = True
            logger.info("MockRM550: Connection successful.")
            return True
        logger.error("MockRM550: Connection failed. Invalid port.")
        return False

    def disconnect(self) -> bool:
        """Simulates disconnecting from the RM550 device."""
        if not self._connected:
            logger.warning("MockRM550: Already disconnected.")
            return True
        self._connected = False
        self._is_enabled = False
        logger.info("MockRM550: Disconnected.")
        return True

    def set_resistance(self, value: float) -> bool:
        """Simulates setting the resistance value."""
        if not self._connected:
            logger.error("MockRM550: Cannot set resistance, not connected.")
            return False

        self._resistance = value
        logger.info(f"MockRM550: Resistance set to {self._resistance:.3f} Ω.")
        return True

    def get_current_resistance(self) -> float:
        """Simulates getting the current resistance value from the device."""
        if not self._connected:
            return 0.0
        # Simulate some minor fluctuation
        return self._resistance + random.uniform(-0.05, 0.05)

    def enable_output(self) -> bool:
        """Simulates enabling the output of the device."""
        if not self._connected:
            logger.error("MockRM550: Cannot enable output, not connected.")
            return False

        self._is_enabled = True
        logger.info("MockRM550: Output enabled.")
        return True

    def disable_output(self) -> bool:
        """Simulates disabling the output of the device."""
        if not self._connected:
            logger.error("MockRM550: Cannot disable output, not connected.")
            return False

        self._is_enabled = False
        logger.info("MockRM550: Output disabled.")
        return True

    def get_output_state(self) -> bool:
        """Simulates getting the current output state."""
        return self._is_enabled
