import sys
import os
import time
from PySide6.QtCore import QCoreApplication, QObject, Signal, Slot, QThread

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir)))

from core.entities.project import Project
from core.entities.power_supply import PowerSupply, PowerSupplyChannel
from core.repositories import Repository
from core.usecases import UseCases
from core.usecases.mocks.mock_power_supply_adapter import MockPowerSupplyAdapter


class MockPowerSupplyPoller(QObject):
    """Mock poller that uses the mock adapter"""
    
    # Signals for communicating with the UI
    polledData = Signal(dict)  # Signal to send polled data to the UI
    error = Signal(str)        # Signal to send error messages to the UI
    finished = Signal()        # Signal to indicate the poller has finished
    
    def __init__(self, project):
        super().__init__()
        self.project = project
        self._running = False
        self._adapter = MockPowerSupplyAdapter()
        
    def start(self):
        """Start the polling loop"""
        self._running = True
        self._poll_loop()
        
    def stop(self):
        """Stop the polling loop"""
        self._running = False
        
    def _poll_loop(self):
        """The main polling loop using mock adapter"""
        try:
            # Create a power supply object for polling
            power_supply = PowerSupply("MOCK::RESOURCE", 9600)
            
            # Open the power supply connection with mock adapter
            self._adapter.open(power_supply)
            
            # Configure the power supply with test values
            from core.entities.power_supply import Channel, IO
            self._adapter.set_voltage_current(power_supply, Channel.CH1, 5.0, 1.0)
            self._adapter.set_voltage_current(power_supply, Channel.CH2, 12.0, 0.5)
            self._adapter.set_voltage_current(power_supply, Channel.CH3, 3.3, 2.0)
            self._adapter.set_on_off(power_supply, IO.ON)
            
            while self._running:
                try:
                    # Poll the power supply data
                    data = self._poll_power_supply(power_supply)
                    
                    # Emit the data signal
                    self.polledData.emit(data)
                    
                    # Process Qt events and sleep for a short time before polling again
                    QCoreApplication.processEvents()
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
        """Poll the power supply for voltage, current, and power data using mock adapter"""
        voltage_data = []
        current_data = []
        power_data = []
        
        # Poll data for each channel
        from core.entities.power_supply import Channel
        channel_names = [Channel.CH1, Channel.CH2, Channel.CH3]
        for i, channel_name in enumerate(channel_names):
            try:
                # Measure voltage
                voltage_str = self._adapter.measure_voltage(power_supply, channel_name)
                voltage = float(voltage_str.strip())
                
                # Measure current
                current_str = self._adapter.measure_current(power_supply, channel_name)
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


class TestPowerSupplyMonitoring(QObject):
    """Test class for power supply monitoring"""
    
    def __init__(self):
        super().__init__()
        self.app = QCoreApplication(sys.argv)
        
        # Create a test project with power supply configuration
        self.project = self._create_test_project()
        
        # Variables to store poller and thread
        self.poller = None
        self.thread = None
        
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
    
    def start_monitoring(self):
        """Start power supply monitoring"""
        print("Starting power supply monitoring...")
        
        try:
            # Create and configure mock power supply poller
            self.poller = MockPowerSupplyPoller(self.project)

            # Connect signals
            self.poller.polledData.connect(self.on_data_received)
            self.poller.error.connect(self.on_error)

            # Create a thread for the poller
            self.thread = QThread()
            self.poller.moveToThread(self.thread)

            # Connect thread signals
            self.thread.started.connect(self.poller.start)
            self.poller.finished.connect(self.thread.quit)
            self.poller.finished.connect(self.poller.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            # Start the thread
            self.thread.start()
            
            # Wait for a while to receive data
            print("Monitoring started, waiting for data...")
            
        except Exception as e:
            print(f"Error starting monitoring: {e}")
            self.app.quit()
    
    def stop_monitoring(self):
        """Stop power supply monitoring"""
        print("Stopping power supply monitoring...")
        
        try:
            # Stop the poller
            if self.poller:
                self.poller.stop()

            # Wait for thread to finish
            if self.thread and self.thread.isRunning():
                self.thread.quit()
                self.thread.wait()
        except Exception as e:
            print(f"Error stopping monitoring: {e}")
        finally:
            # Quit the application
            self.app.quit()
    
    def run(self):
        """Run the test"""
        print("Power Supply Monitoring Test")
        print("===========================")
        
        # Start monitoring
        self.start_monitoring()
        
        # Run the Qt event loop
        return self.app.exec()


if __name__ == "__main__":
    test = TestPowerSupplyMonitoring()
    sys.exit(test.run())