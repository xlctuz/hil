from PySide6.QtCore import QObject, Property, Slot, QAbstractListModel, QModelIndex, Qt, Signal, QThread, QTimer

class PowerSupplyChannelProxy(QObject):
    def __init__(self, channel_data, parent=None):
        super().__init__(parent)
        self._channel_data = channel_data

    @Property('QVariant', constant=True)
    def voltage(self):
        return self._channel_data.voltage if self._channel_data and self._channel_data.voltage is not None else None

    @Property('QVariant', constant=True)
    def current(self):
        return self._channel_data.current if self._channel_data and self._channel_data.current is not None else None


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


