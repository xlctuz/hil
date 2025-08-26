from abc import ABC, abstractmethod

class RM550Port(ABC):
    """Abstract port for RM550 device interaction."""

    @abstractmethod
    def connect(self, port: str, baudrate: int) -> bool:
        """Connects to the RM550 device."""
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnects from the RM550 device."""
        pass

    @abstractmethod
    def set_resistance(self, value: float) -> bool:
        """Sets the resistance value."""
        pass

    @abstractmethod
    def get_current_resistance(self) -> float:
        """Gets the current resistance value from the device."""
        pass

    @abstractmethod
    def enable_output(self) -> bool:
        """Enables the output of the device."""
        pass

    @abstractmethod
    def disable_output(self) -> bool:
        """Disables the output of the device."""
        pass

    @abstractmethod
    def get_output_state(self) -> bool:
        """Gets the current output state (enabled/disabled)."""
        pass
