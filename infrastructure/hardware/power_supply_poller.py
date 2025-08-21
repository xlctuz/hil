import time
from PySide6.QtCore import QObject, Signal, QThread
from infrastructure.hardware.power_supply_adapter import PowerSupplyAdapter
from contextlib import contextmanager


class PowerSupplyPoller(QObject):
    # Signals for communicating with the UI
    polledData = Signal(dict)  # Signal to send polled data to the UI
    error = Signal(str)        # Signal to send error messages to the UI
    finished = Signal()        # Signal to indicate the poller has finished

    def __init__(self, resource_name, baud_rate, project):
        super().__init__()
        self.resource_name = resource_name
        self.baud_rate = baud_rate
        self.project = project
        self._running = False
        self._adapter = PowerSupplyAdapter()

    def start(self):
        """Start the polling loop in a separate thread"""
        self._running = True
        self._poll_loop()

    def stop(self):
        """Stop the polling loop"""
        self._running = False

    def _poll_loop(self):
        """The main polling loop"""
        try:
            # Create a power supply object for polling
            from domain.models.power_supply import PowerSupply
            power_supply = PowerSupply(self.resource_name, self.baud_rate)
            
            # Open the power supply connection
            self._adapter.open(power_supply)
            
            while self._running:
                try:
                    # Poll the power supply data
                    data = self._poll_power_supply(power_supply)
                    
                    # Emit the data signal
                    self.polledData.emit(data)
                    
                    # Sleep for a short time before polling again
                    # In a real application, this might be configurable
                    QThread.msleep(1000)  # 1 second
                except Exception as e:
                    # Emit error signal
                    self.error.emit(f"Error polling power supply: {str(e)}")
                    # Stop polling on error
                    self._running = False
                    
        except Exception as e:
            # Emit error signal for connection issues
            self.error.emit(f"Error connecting to power supply: {str(e)}")
        finally:
            # Close the power supply connection
            try:
                self._adapter.close(power_supply)
            except:
                pass  # Ignore errors when closing
            
            # Emit finished signal
            self.finished.emit()

    def _poll_power_supply(self, power_supply):
        """Poll the power supply for voltage, current, and power data"""
        voltage_data = []
        current_data = []
        power_data = []
        
        # Poll data for each channel
        for i, channel in enumerate(self.project.power_supply.channels):
            try:
                # Measure voltage
                voltage_str = self._adapter.measure_voltage(power_supply, channel)
                voltage = float(voltage_str.strip())
                
                # Measure current
                current_str = self._adapter.measure_current(power_supply, channel)
                current = float(current_str.strip())
                
                # Calculate power
                power = voltage * current
                
                # Add data to lists
                voltage_data.append(voltage)
                current_data.append(current)
                power_data.append(power)
            except Exception as e:
                # If there's an error reading a channel, use None values
                voltage_data.append(None)
                current_data.append(None)
                power_data.append(None)
                print(f"Error reading channel {i+1}: {str(e)}")
        
        # Return the data as a dictionary
        return {
            'voltage': voltage_data,
            'current': current_data,
            'power': power_data
        }