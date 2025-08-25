from PySide6.QtCore import QObject, Property, Signal, QAbstractListModel, QModelIndex, Qt
from core.entities.pcie_1762h import Status


class DioChannelViewModel(QObject):
    statusChanged = Signal()

    def __init__(self, channel_data, parent=None):
        super().__init__(parent)
        self._channel_data = channel_data
        self._status = Status.NA  # DI channels manage their own status in the view

    @Property(str, notify=statusChanged)
    def status(self):
        # For DO channels, reflect the database state. For DI, reflect the live state.
        if hasattr(self._channel_data, 'status'):
            return self._channel_data.status.value
        return self._status.value

    @status.setter
    def status(self, value):
        new_status = Status(value)
        if hasattr(self._channel_data, 'status'):
            self._channel_data.status = new_status
        else:
            self._status = new_status
        self.statusChanged.emit()

    @Property(str, constant=True)
    def name(self):
        return self._channel_data.name


class DioViewModel(QObject):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._pcie_1762h_data = data
        self._do_channels = [DioChannelViewModel(ch) for ch in data.do_channels] if data else []
        self._di_channels = [DioChannelViewModel(ch) for ch in data.di_channels] if data else []
        # DI echos are just view models for displaying DI state, not representing persistent data
        self._di_echos = [DioChannelViewModel(ch) for ch in data.di_channels] if data else []

    @Property('QVariant', constant=True)
    def doChannels(self):
        return self._do_channels

    @Property('QVariant', constant=True)
    def diChannels(self):
        return self._di_channels

    @Property('QVariant', constant=True)
    def diEchos(self):
        return self._di_echos

    @Property('QVariant', constant=True)
    def configuredDoChannels(self):
        return [ch for ch in self._do_channels if ch.name]

    @Property('QVariant', constant=True)
    def configuredDiEchos(self):
        # The echos correspond to DI channels, so we filter based on the original DI channel name
        return [echo for i, echo in enumerate(self._di_echos) if self._di_channels[i].name]

    def update_di_status(self, di_data):
        """Updates the status of the DI echo channels based on the integer data."""
        for i in range(16):
            bit_value = (di_data >> i) & 1
            status = Status.HIGH if bit_value else Status.LOW
            if i < len(self._di_echos):
                # Check if status is different to avoid unnecessary signals
                if self._di_echos[i].status != status.value:
                    self._di_echos[i].status = status.value