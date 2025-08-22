from core.interfaces.power_supply_port import PowerSupplyPort
from core.entities.power_supply import PowerSupply, IO, Channel
import random


class MockPowerSupplyAdapter(PowerSupplyPort):
    """Mock adapter for power supply testing"""
    
    def __init__(self):
        self._connected = False
        self._output_on = False
        self._channels = {
            1: {"voltage_set": 0.0, "current_set": 0.0, "voltage_meas": 0.0, "current_meas": 0.0},
            2: {"voltage_set": 0.0, "current_set": 0.0, "voltage_meas": 0.0, "current_meas": 0.0},
            3: {"voltage_set": 0.0, "current_set": 0.0, "voltage_meas": 0.0, "current_meas": 0.0}
        }
    
    def open(self, power_supply: PowerSupply):
        """Open connection to the mock power supply"""
        self._connected = True
        power_supply.instrument = self  # Store self as instrument for compatibility
    
    def close(self, power_supply: PowerSupply):
        """Close connection to the mock power supply"""
        self._connected = False
        if hasattr(power_supply, 'instrument'):
            delattr(power_supply, 'instrument')
    
    def set_voltage(self, power_supply: PowerSupply, channel: int, voltage: float):
        """Set voltage for a channel"""
        if not self._connected:
            raise Exception("Power supply not connected")
        if channel not in self._channels:
            raise Exception(f"Invalid channel {channel}")
        
        self._channels[channel]["voltage_set"] = voltage
        # When output is on, update measured voltage to be close to set voltage
        if self._output_on:
            self._channels[channel]["voltage_meas"] = voltage + random.uniform(-0.1, 0.1)
    
    def get_voltage(self, power_supply: PowerSupply, channel: int) -> float:
        """Get voltage for a channel"""
        if not self._connected:
            raise Exception("Power supply not connected")
        if channel not in self._channels:
            raise Exception(f"Invalid channel {channel}")
        
        return self._channels[channel]["voltage_set"]
    
    def set_current(self, power_supply: PowerSupply, channel: int, current: float):
        """Set current for a channel"""
        if not self._connected:
            raise Exception("Power supply not connected")
        if channel not in self._channels:
            raise Exception(f"Invalid channel {channel}")
        
        self._channels[channel]["current_set"] = current
        # When output is on, update measured current to be close to set current
        if self._output_on:
            self._channels[channel]["current_meas"] = current + random.uniform(-0.01, 0.01)
    
    def get_current(self, power_supply: PowerSupply, channel: int) -> float:
        """Get current for a channel"""
        if not self._connected:
            raise Exception("Power supply not connected")
        if channel not in self._channels:
            raise Exception(f"Invalid channel {channel}")
        
        return self._channels[channel]["current_set"]
    
    def set_voltage_current(self, power_supply: PowerSupply, channel: Channel, voltage: float, current: float):
        """Set both voltage and current for a channel"""
        # Convert channel to integer (1-based indexing)
        if channel == Channel.ALL:
            channel_int = 1
        else:
            # Extract channel number from Channel enum (CH1, CH2, CH3)
            channel_int = int(channel.name[-1])
        
        self.set_voltage(power_supply, channel_int, voltage)
        self.set_current(power_supply, channel_int, current)
    
    def measure_current(self, power_supply: PowerSupply, channel: Channel = Channel.ALL) -> str:
        """Measure current for a channel"""
        if not self._connected:
            raise Exception("Power supply not connected")
        
        # Convert channel to integer (1-based indexing)
        if channel == Channel.ALL:
            # For simplicity, return data for channel 1 when ALL is requested
            channel_int = 1
        else:
            # Extract channel number from Channel enum (CH1, CH2, CH3)
            channel_int = int(channel.name[-1])
        
        if channel_int not in self._channels:
            raise Exception(f"Invalid channel {channel_int}")
        
        # Add some noise to the measurement
        measured = self._channels[channel_int]["current_meas"]
        noise = random.uniform(-0.005, 0.005)
        return f"{measured + noise:.6f}"
    
    def measure_voltage(self, power_supply: PowerSupply, channel: Channel = Channel.ALL) -> str:
        """Measure voltage for a channel"""
        if not self._connected:
            raise Exception("Power supply not connected")
        
        # Convert channel to integer (1-based indexing)
        if channel == Channel.ALL:
            # For simplicity, return data for channel 1 when ALL is requested
            channel_int = 1
        else:
            # Extract channel number from Channel enum (CH1, CH2, CH3)
            channel_int = int(channel.name[-1])
        
        if channel_int not in self._channels:
            raise Exception(f"Invalid channel {channel_int}")
        
        # Add some noise to the measurement
        measured = self._channels[channel_int]["voltage_meas"]
        noise = random.uniform(-0.05, 0.05)
        return f"{measured + noise:.6f}"
    
    def measure_power(self, power_supply: PowerSupply, channel: Channel = Channel.ALL) -> str:
        """Measure power for a channel"""
        voltage_str = self.measure_voltage(power_supply, channel)
        current_str = self.measure_current(power_supply, channel)
        
        voltage = float(voltage_str)
        current = float(current_str)
        power = voltage * current
        
        return f"{power:.6f}"
    
    def set_on_off(self, power_supply: PowerSupply, io: IO, channel: Channel = Channel.ALL):
        """Turn output on or off"""
        if not self._connected:
            raise Exception("Power supply not connected")
        
        if io == IO.ON:
            self._output_on = True
            # When turning on, update measured values to be close to set values
            for ch in self._channels.values():
                ch["voltage_meas"] = ch["voltage_set"] + random.uniform(-0.1, 0.1)
                ch["current_meas"] = ch["current_set"] + random.uniform(-0.01, 0.01)
        else:
            self._output_on = False
            # When turning off, set measured values to 0
            for ch in self._channels.values():
                ch["voltage_meas"] = 0.0
                ch["current_meas"] = 0.0