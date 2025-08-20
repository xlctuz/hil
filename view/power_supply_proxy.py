from PySide6.QtCore import QObject, Property, Slot, QAbstractListModel, QModelIndex, Qt, Signal, QThread, QTimer

class PowerSupplyChannelProxy(QObject):
    voltageChanged = Signal(float)
    currentChanged = Signal(float)
    powerChanged = Signal(float)

    def __init__(self, channel_data, parent=None):
        super().__init__(parent)
        self._channel_data = channel_data
        self._measured_voltage = 0.0
        self._measured_current = 0.0
        self._measured_power = 0.0

    @Property(float, notify=voltageChanged)
    def voltage(self):
        return self._channel_data.voltage if self._channel_data and self._channel_data.voltage is not None else 0.0

    @Property(float, notify=currentChanged)
    def current(self):
        return self._channel_data.current if self._channel_data and self._channel_data.current is not None else 0.0

    @Property(float, notify=powerChanged)
    def power(self):
        return self._measured_power

    @Property(float, notify=voltageChanged)
    def measuredVoltage(self):
        return self._measured_voltage

    @Property(float, notify=currentChanged)
    def measuredCurrent(self):
        return self._measured_current

    @Property(int, constant=True)
    def index(self):
        return self._channel_data.index if self._channel_data else -1

    @Property(bool, constant=True)
    def isConfigured(self):
        return self._channel_data and (self._channel_data.voltage is not None or self._channel_data.current is not None)

    def updateMeasurements(self, voltage, current, power):
        self._measured_voltage = voltage
        self._measured_current = current
        self._measured_power = power
        self.voltageChanged.emit(voltage)
        self.currentChanged.emit(current)
        self.powerChanged.emit(power)


class PowerSupplyProxy(QObject):
    resourceNameChanged = Signal()
    baudRateChanged = Signal()

    def __init__(self, power_supply_data, parent=None):
        super().__init__(parent)
        self._power_supply_data = power_supply_data
        self._channels = []
        if self._power_supply_data:
            # sort channels by index
            sorted_channels = sorted(self._power_supply_data.channels, key=lambda c: c.index)
            for ch_data in sorted_channels:
                self._channels.append(PowerSupplyChannelProxy(ch_data, self))
                # ensure 3 channels exist for QML binding
        while len(self._channels) < 3:
            self._channels.append(PowerSupplyChannelProxy(None, self))

    @Property(str, notify=resourceNameChanged)
    def resource_name(self):
        return self._power_supply_data.resource_name if self._power_supply_data else ""

    @Property(int, notify=baudRateChanged)
    def baud_rate(self):
        return self._power_supply_data.baud_rate if self._power_supply_data else 9600

    @Property(QObject, constant=True)
    def ch1(self):
        return self._channels[0]

    @Property(QObject, constant=True)
    def ch2(self):
        return self._channels[1]

    @Property(QObject, constant=True)
    def ch3(self):
        return self._channels[2]

    @Property('QVariant', constant=True)
    def configuredChannels(self):
        if not self._power_supply_data:
            return []
        return [ch for ch in self._channels if ch.isConfigured]






