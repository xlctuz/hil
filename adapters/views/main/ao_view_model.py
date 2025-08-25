from PySide6.QtCore import QObject, Property, Signal


class AoChannelViewModel(QObject):
    def __init__(self, channel_data, parent=None):
        super().__init__(parent)
        self._channel_data = channel_data

    @Property(str, constant=True)
    def name(self):
        return self._channel_data.name if self._channel_data else ""

    @Property(float, constant=True)
    def voltage(self):
        return self._channel_data.voltage if self._channel_data and self._channel_data.voltage is not None else 0.0

    @Property(int, constant=True)
    def index(self):
        return self._channel_data.index if self._channel_data else -1


class AoViewModel(QObject):
    def __init__(self, pci1720u_data, parent=None):
        super().__init__(parent)
        self._pci1720u_data = pci1720u_data
        self._channels = []
        if self._pci1720u_data:
            sorted_channels = sorted(self._pci1720u_data.channels, key=lambda c: c.index)
            # Filter for only configured channels (those with a name)
            self._channels = [AoChannelViewModel(ch) for ch in sorted_channels if ch.name]

    @Property('QVariant', constant=True)
    def configuredChannels(self):
        return self._channels
