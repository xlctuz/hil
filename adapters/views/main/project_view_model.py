from PySide6.QtCore import QObject, Property, Slot, Signal, QThread, QTimer
from adapters.views.main.power_supply_view_model import PowerSupplyViewModel
from adapters.views.main.dio_view_model import DioViewModel
from adapters.devices.pcie_1762h_adapter import Pcie1762hAdapter
from core.entities.power_supply import IO
from core.entities.pcie_1762h import Status
from core.logger import logger
from core.usecases import UseCases


class ProjectViewModel(QObject):
    # Signals for communicating with UI
    voltageDataChanged = Signal(list)
    currentDataChanged = Signal(list)
    powerDataChanged = Signal(list)
    dioDataChanged = Signal(int)
    errorOccurred = Signal(str)
    started = Signal()
    stopped = Signal()

    def __init__(self, project_data, parent=None):
        super().__init__(parent)
        self._project_data = project_data
        self._power_supply = PowerSupplyViewModel(project_data.power_supply if project_data else None, self)
        self._pcie_1762h = DioViewModel(project_data.pcie_1762h if project_data else None, self)
        self._is_started = False

        # Hardware adapters
        self._pcie_1762h_adapter = Pcie1762hAdapter()

        # Poller for power supply data
        self._power_supply_poller = None
        self._poller_thread = None

        # Timer for DIO monitoring
        self._dio_timer = None

    @Property('QVariant', constant=True)
    def name(self):
        return self._project_data.name if self._project_data else None

    @Property(QObject, constant=True)
    def powerSupply(self):
        return self._power_supply

    @Property(QObject, constant=True)
    def pcie1762h(self):
        return self._pcie_1762h

    @Property(bool, constant=True)
    def is_started(self):
        return self._is_started


    @Slot(result=bool)
    def start(self):
        """Start the project: configure hardware devices and start monitoring"""
        if not self._project_data or self._is_started:
            return False

        try:
            # Configure power supply
            self._configure_power_supply()

            # Configure DIO
            self._configure_dio()

            # Start monitoring
            self._start_monitoring()

            self._is_started = True
            self.started.emit()
            return True
        except Exception as e:
            logger.error(f"Error starting project: {str(e)}")
            self.errorOccurred.emit(f"启动项目失败: {str(e)}")
            self.stop()  # Clean up any partially started components
            return False

    @Slot()
    def stop(self):
        """Stop the project: stop monitoring and turn off devices"""
        if not self._is_started:
            return

        try:
            # Stop monitoring
            self._stop_monitoring()

            # Turn off power supply
            self._turn_off_power_supply()

            self._is_started = False
            self.stopped.emit()
        except Exception as e:
            logger.error(f"Error stopping project: {str(e)}")
            self.errorOccurred.emit(f"停止项目失败: {str(e)}")
        finally:
            # Ensure started state is False even if there was an error
            self._is_started = False

    def _configure_power_supply(self):
        """Configure the power supply with project settings"""
        if not self._project_data.power_supply:
            return

        try:
            power_supply = self._project_data.power_supply
            # Create a temporary power supply object for configuration
            from core.entities.power_supply import PowerSupply, Channel
            temp_power_supply = PowerSupply(power_supply.resource_name, power_supply.baud_rate)

            # Open connection
            self.usecases.power_supply_port.open(temp_power_supply)

            try:
                # Map channel indices to Channel enum values
                channel_map = {0: Channel.CH1, 1: Channel.CH2, 2: Channel.CH3}
                
                # Configure each channel
                for channel in power_supply.channels:
                    if channel.voltage is not None and channel.current is not None:
                        # Get the corresponding Channel enum value
                        channel_enum = channel_map.get(channel.index, Channel.CH1)
                        
                        # Apply voltage and current settings
                        self.usecases.power_supply_port.set_voltage_current(
                            temp_power_supply,
                            channel_enum,
                            channel.voltage,
                            channel.current
                        )

                # Turn on power supply
                self.usecases.power_supply_port.set_on_off(temp_power_supply, IO.ON)
            finally:
                # Close connection
                self.usecases.power_supply_port.close(temp_power_supply)
        except Exception as e:
            raise Exception(f"配置电源失败: {str(e)}")

    def _configure_dio(self):
        """Configure the DIO with project settings"""
        if not self._project_data.pcie_1762h:
            return

        try:
            # Set DO channels according to project configuration
            self._pcie_1762h_adapter.run_test(self._project_data.pcie_1762h)
        except Exception as e:
            raise Exception(f"配置DIO失败: {str(e)}")

    def _turn_off_power_supply(self):
        """Turn off the power supply"""
        if not self._project_data.power_supply:
            return

        try:
            power_supply = self._project_data.power_supply
            # Create a temporary power supply object for configuration
            from core.entities.power_supply import PowerSupply, Channel
            temp_power_supply = PowerSupply(power_supply.resource_name, power_supply.baud_rate)

            # Open connection
            self.usecases.power_supply_port.open(temp_power_supply)

            try:
                # Turn off power supply
                self.usecases.power_supply_port.set_on_off(temp_power_supply, IO.OFF)
            finally:
                # Close connection
                self.usecases.power_supply_port.close(temp_power_supply)
        except Exception as e:
            logger.error(f"Error turning off power supply: {str(e)}")

    def _start_monitoring(self):
        """Start monitoring power supply and DIO status"""
        if not self._project_data.power_supply:
            return

        try:
            # Use the use case to start power supply monitoring
            self._power_supply_poller, self._poller_thread = self.usecases.start_power_supply_monitoring(
                self._project_data,
                self._on_power_data_polled,
                self._on_polling_error
            )

            # Start DIO monitoring with a timer
            self._start_dio_monitoring()
        except Exception as e:
            raise Exception(f"启动监控失败: {str(e)}")

    def _start_dio_monitoring(self):
        """Start monitoring DIO status with a timer"""
        if not self._project_data.pcie_1762h:
            return

        try:
            self._dio_timer = QTimer()
            self._dio_timer.timeout.connect(self._read_dio_status)
            self._dio_timer.start(500)  # Read DIO status every 500ms
        except Exception as e:
            raise Exception(f"启动DIO监控失败: {str(e)}")

    def _stop_dio_monitoring(self):
        """Stop monitoring DIO status"""
        if self._dio_timer:
            self._dio_timer.stop()
            self._dio_timer.deleteLater()
            self._dio_timer = None

    def _stop_monitoring(self):
        """Stop monitoring power supply and DIO status"""
        try:
            # Use the use case to stop power supply monitoring
            self.usecases.stop_power_supply_monitoring(self._power_supply_poller, self._poller_thread)

            # Stop DIO monitoring
            self._stop_dio_monitoring()
        except Exception as e:
            logger.error(f"Error stopping monitoring: {str(e)}")

    def _on_power_data_polled(self, data):
        """Handle polled power supply data"""
        try:
            # Emit signals with the data
            self.voltageDataChanged.emit(data.get('voltage', []))
            self.currentDataChanged.emit(data.get('current', []))
            self.powerDataChanged.emit(data.get('power', []))

            # Update power supply proxy with measured values
            voltage_data = data.get('voltage', [])
            current_data = data.get('current', [])
            power_data = data.get('power', [])

            # Update each channel's measurements
            for i, channel_proxy in enumerate(self._power_supply._channels):
                if i < len(voltage_data) and i < len(current_data) and i < len(power_data):
                    voltage = voltage_data[i] if voltage_data[i] is not None else 0.0
                    current = current_data[i] if current_data[i] is not None else 0.0
                    power = power_data[i] if power_data[i] is not None else 0.0
                    channel_proxy.updateMeasurements(voltage, current, power)
        except Exception as e:
            logger.error(f"Error handling power data: {str(e)}")

    def _read_dio_status(self):
        """Read DIO status and update UI"""
        if not self._project_data.pcie_1762h:
            return

        try:
            # Read DI status
            di_data = self._pcie_1762h_adapter.get_di(self._project_data.pcie_1762h)

            # Update DI echo channels
            for i in range(16):
                # Extract bit i from di_data
                bit_value = (di_data >> i) & 1
                status = Status.HIGH if bit_value else Status.LOW

                # Update the echo channel
                if i < len(self._pcie_1762h._di_echos):
                    self._pcie_1762h._di_echos[i].status = status.value

            # Emit signal with DI data
            self.dioDataChanged.emit(di_data)
        except Exception as e:
            logger.error(f"Error reading DIO status: {str(e)}")
            self.errorOccurred.emit(f"读取DIO状态失败: {str(e)}")

    def _on_polling_error(self, error_message):
        """Handle polling error"""
        logger.error(f"Polling error: {error_message}")
        self.errorOccurred.emit(error_message)
        # Stop the project on polling error
        self.stop()
