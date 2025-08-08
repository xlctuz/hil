from enum import Enum
from PySide6.QtCore import QObject, Property, Slot, QAbstractListModel, QModelIndex, Qt, Signal, QThread, QTimer

class DioChannelType(Enum):
    DO = 0
    DI = 1


class DioChannelProxy(QObject):
    statusNotify = Signal(str)

    def __init__(self, channel_data, channel_type, parent=None):
        super().__init__(parent)
        self._channel_data = channel_data
        self._channel_type = channel_type

    @Property(int, constant=True)
    def index(self):
        return self._channel_data.index if self._channel_data else -1

    @Property(str, constant=True)
    def name(self):
        return self._channel_data.name if self._channel_data else ""

    @Property(str, notify=statusNotify)
    def status(self):
        return self._channel_data.status.value if self._channel_data and self._channel_data.status else ""

    @status.setter
    def status(self, value):
        if self._channel_data.status.value != value:
            self._channel_data.status.value = value
            self.statusNotify.emit(value)

class Pcie1762hProxy(QObject):
    def __init__(self, pcie_data, parent=None):
        super().__init__(parent)
        self._pcie_data = pcie_data
        self._do_channels = []
        self._di_channels = []

        if self._pcie_data:
            # sort channels by index
            sorted_do = sorted(self._pcie_data.do_channels, key=lambda c: c.index)
            sorted_di = sorted(self._pcie_data.di_channels, key=lambda c: c.index)

            for ch_data in sorted_do:
                self._do_channels.append(DioChannelProxy(ch_data, DioChannelType.DO, self))
            for ch_data in sorted_di:
                self._di_channels.append(DioChannelProxy(ch_data, DioChannelType.DI, self))

    @Property('QVariant', constant=True)
    def doChannels(self):
        return self._do_channels

    @Property('QVariant', constant=True)
    def diChannels(self):
        return self._di_channels
