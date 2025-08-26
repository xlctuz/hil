from PySide6.QtCore import QObject, Property, Slot, Signal
from adapters.views.main.power_supply_view_model import PowerSupplyViewModel
from adapters.views.main.dio_view_model import DioViewModel
from adapters.views.main.ao_view_model import AoViewModel
from adapters.views.main.rm550_view_model import RM550ViewModel
from core.logger import logger
from core.usecases import UseCases
import traceback

class ProjectViewModel(QObject):
    # Signals for communicating with UI
    voltageDataChanged = Signal(list)
    currentDataChanged = Signal(list)
    powerDataChanged = Signal(list)
    dioDataChanged = Signal(int)
    errorOccurred = Signal(str)
    started = Signal()
    stopped = Signal()

    def __init__(self, usecases: UseCases, project_data, parent=None):
        super().__init__(parent)
        self.usecases = usecases
        self._project_data = project_data
        self._power_supply = PowerSupplyViewModel(project_data.power_supply if project_data else None, self)
        self._pcie_1762h = DioViewModel(project_data.pcie_1762h if project_data else None, self)
        self._pci1720u = AoViewModel(project_data.pci1720u if project_data else None, self)
        # Create the RM550 ViewModel
        self._rm550 = RM550ViewModel(self.usecases.toggle_rm550_output)
        self._is_started = False

        # Schedulers for monitoring
        self._power_supply_scheduler = None
        self._dio_scheduler = None
        self._rm550_scheduler = None

    @Property('QVariant', constant=True)
    def name(self):
        return self._project_data.name if self._project_data else None

    @Property(QObject, constant=True)
    def powerSupply(self):
        return self._power_supply

    @Property(QObject, constant=True)
    def pcie1762h(self):
        return self._pcie_1762h

    @Property(QObject, constant=True)
    def pci1720u(self):
        return self._pci1720u

    @Property(QObject, constant=True)
    def rm550(self):
        return self._rm550

    @Property(bool, constant=True)
    def is_started(self):
        return self._is_started

    @Slot(result=bool)
    def start(self):
        """Start the project: configure hardware devices and start monitoring"""
        if not self._project_data or self._is_started:
            return False

        try:
            self.usecases.start_project(self._project_data)
            self._start_monitoring()
            self._is_started = True
            self.started.emit()
            return True
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Error starting project: {str(e)}")
            self.errorOccurred.emit(f"启动项目失败: {str(e)}")
            self.stop()
            return False

    @Slot()
    def stop(self):
        """Stop the project: stop monitoring and turn off devices"""
        if not self._is_started:
            return

        try:
            self._stop_monitoring()
            self.usecases.stop_project(self._project_data)
            self._is_started = False
            self.stopped.emit()
        except Exception as e:
            logger.error(f"Error stopping project: {str(e)}")
            self.errorOccurred.emit(f"停止项目失败: {str(e)}")
        finally:
            self._is_started = False

    def _start_monitoring(self):
        """Start monitoring all relevant hardware"""
        try:
            # Start power supply monitoring
            if self._project_data.power_supply:
                self._power_supply_scheduler = self.usecases.start_power_supply_monitoring(
                    self._project_data,
                    self._on_power_data_polled,
                    self._on_polling_error
                )

            # Start DIO monitoring
            if self._project_data.pcie_1762h:
                self._dio_scheduler = self.usecases.start_pcie_1762h_monitoring(
                    self._project_data,
                    self._on_dio_data_polled,
                    self._on_polling_error
                )
            # ... (power supply and DIO monitoring startups remain the same)

            # Start RM550 monitoring
            self.usecases.start_rm550_monitoring.execute(self._on_rm550_data_polled)

        except Exception as e:
            raise Exception(f"启动监控失败: {str(e)}")

    def _stop_monitoring(self):
        """Stop all monitoring tasks"""
        try:
            # Stop power supply monitoring
            self.usecases.stop_power_supply_monitoring(self._power_supply_scheduler)
            self._power_supply_scheduler = None
            # ... (power supply and DIO monitoring stops remain the same)

            # Stop RM550 monitoring
            self.usecases.stop_rm550_monitoring.execute()

            # Stop DIO monitoring
            self.usecases.stop_pcie_1762h_monitoring(self._dio_scheduler)
            self._dio_scheduler = None
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

    def _on_dio_data_polled(self, di_data):
        """Handle polled DIO data"""
        try:
            # Update the view model
            self._pcie_1762h.update_di_status(di_data)

            # Emit signal with DI data for other UI components if needed
            self.dioDataChanged.emit(di_data)
        except Exception as e:
            logger.error(f"Error handling DIO data: {str(e)}")
            self.errorOccurred.emit(f"处理DIO数据失败: {str(e)}")

    def _on_rm550_data_polled(self, resistance, is_enabled):
        """Handle polled RM550 data"""
        try:
            self._rm550.update_data(resistance, is_enabled)
        except Exception as e:
            logger.error(f"Error handling RM550 data: {str(e)}")
            self.errorOccurred.emit(f"处理RM550数据失败: {str(e)}")

    def _on_polling_error(self, error_message):
        """Handle polling error"""
        logger.error(f"Polling error: {error_message}")
        self.errorOccurred.emit(error_message)
        # Stop the project on polling error
        self.stop()
