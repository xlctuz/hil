from core.interfaces.rm550_port import RM550Port
from adapters.devices.rm550_controller import RM550Controller
from core.logger import logger

class RM550Adapter(RM550Port):
    """Adapter for the RM550 Controller to be used in the application's core."""

    def __init__(self):
        self.controller: RM550Controller = None
        self._is_enabled = False

    def connect(self, port: str, baudrate: int) -> bool:
        """Initializes and connects to the RM550 device."""
        try:
            self.controller = RM550Controller(port=port, baudrate=baudrate)
            if self.controller.connect():
                logger.info(f"Successfully connected to RM550 on {port}.")
                return True
            else:
                self.controller = None
                logger.error(f"Failed to connect to RM550 on {port}.")
                return False
        except Exception as e:
            self.controller = None
            logger.error(f"Exception during RM550 connection: {e}")
            return False

    def disconnect(self) -> bool:
        """Disconnects from the RM550 device."""
        if self.controller:
            self.controller.disconnect()
            self.controller = None
            self._is_enabled = False
            logger.info("RM550 disconnected.")
        return True

    def set_resistance(self, value: float) -> bool:
        """Sets the resistance value."""
        if not self.controller:
            logger.warning("Cannot set resistance: RM550 not connected.")
            return False
        
        response = self.controller.set_setpoint_resistance(value)
        if response and 'SP(R)' in response:
            logger.info(f"Successfully set RM550 resistance to {response['SP(R)']:.3f} Ω.")
            return True
        else:
            logger.error(f"Failed to set RM550 resistance to {value} Ω.")
            return False

    def get_current_resistance(self) -> float:
        """Gets the current resistance value (PV) from the device."""
        if not self.controller:
            return 0.0
        
        info = self.controller.get_output_resistance_info()
        if info and 'PV(R)' in info:
            return info['PV(R)']
        return 0.0

    def enable_output(self) -> bool:
        """Enables the output of the device by closing the main path relay."""
        if not self.controller:
            logger.warning("Cannot enable output: RM550 not connected.")
            return False
        
        response = self.controller.connect_main_path_relay()
        if response:
            self._is_enabled = True
            logger.info("RM550 output enabled.")
            return True
        else:
            logger.error("Failed to enable RM550 output.")
            return False

    def disable_output(self) -> bool:
        """Disables the output of the device by opening the main path relay."""
        if not self.controller:
            logger.warning("Cannot disable output: RM550 not connected.")
            return False
            
        response = self.controller.disconnect_main_path_relay()
        if response:
            self._is_enabled = False
            logger.info("RM550 output disabled.")
            return True
        else:
            logger.error("Failed to disable RM550 output.")
            return False

    def get_output_state(self) -> bool:
        """
        Gets the current output state.
        Note: This returns the cached state within the adapter, as the device
        itself does not seem to have a direct command to query the relay state.
        """
        return self._is_enabled
