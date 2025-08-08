from PySide6.QtCore import QObject, Property, Slot, QAbstractListModel, QModelIndex, Qt, Signal, QThread, QTimer
from core.power_supply_it6302 import Power_supply_it6302, Power_supply_it6302_channel, IO, Channel as PSChannel
import traceback

class PowerSupplyPoller(QObject):
    polledData = Signal(dict)
    finished = Signal()
    error = Signal(str)

    def __init__(self, resource_name, baud_rate, project, parent=None):
        super().__init__(parent)
        self._resource_name = resource_name
        self._baud_rate = baud_rate
        self._project = project
        self._ps_controller = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.poll)
        self._running = False

    def start(self):
        try:
            self._ps_controller = Power_supply_it6302(resource_name = self._resource_name, baud_rate = self._baud_rate)
            self._ps_controller.open()

            # Set initial configuration from the project
            ps_config = self._project.power_supply
            for i, ch_config in enumerate(ps_config.channels):
                channel_enum = PSChannel[f"CH{i+1}"]
                if ch_config.voltage is not None and ch_config.current is not None:
                    self._ps_controller.set_voltage_current(channel_enum, ch_config.voltage, ch_config.current)
                    self._ps_controller.set_on_off(IO.ON, channel_enum)

            self._running = True
            self._timer.start(100) # 100 ms interval
            print("Poller started and power supply configured.")
        except Exception as e:
            traceback.print_exc()
            self.error.emit(f"Failed to start poller: {e}")
            self.stop()

    def stop(self):
        self._running = False
        self._timer.stop()
        if self._ps_controller:
            try:
                # Turn off all channels when polling stops
                self._ps_controller.set_on_off(IO.OFF, PSChannel.ALL)
                if self._ps_controller.instrument and self._ps_controller.instrument.session is not None:
                    self._ps_controller.close()
            except Exception as e:
                print(f"Error while closing power supply in poller: {e}")

        self._ps_controller = None
        self.finished.emit()
        print("Poller stopped.")

    def poll(self):
        if not self._running or not self._ps_controller:
            return

        try:
            data = {
                'voltage': [],
                'current': [],
                'power': []
            }
            channels = [PSChannel.CH1, PSChannel.CH2, PSChannel.CH3]
            for ch in channels:
                v_str = self._ps_controller.measure_voltage(ch).strip()
                c_str = self._ps_controller.measure_current(ch).strip()
                p_str = self._ps_controller.measure_power(ch).strip()

                data['voltage'].append(float(v_str) if v_str else 0.0)
                data['current'].append(float(c_str) if c_str else 0.0)
                data['power'].append(float(p_str) if p_str else 0.0)

            self.polledData.emit(data)
        except Exception as e:
            self.error.emit(f"Polling failed: {e}")
            self.stop()
