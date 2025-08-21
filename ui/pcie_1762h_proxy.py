from enum import Enum
from PySide6.QtCore import QObject, Property, Slot, Signal
from base.models.pcie_1762h import Status
from core.use_cases import use_cases
from base.logger import logger
import traceback


class DioChannelType(Enum):
    DO = 0
    DI = 1


class DioChannelProxy(QObject):
    statusNotify = Signal(str)
    nameNotify = Signal(str)

    def __init__(self, channel_data, channel_type, parent=None):
        super().__init__(parent)
        self._channel_data = channel_data
        self._channel_type = channel_type

    @Property(int, constant=True)
    def index(self):
        return self._channel_data.index if self._channel_data else -1

    @Property(str, notify=nameNotify)
    def name(self):
        return self._channel_data.name if self._channel_data else ""

    @name.setter
    def name(self, value):
        if self._channel_data.name != value:
            self._channel_data.name = value
            self.nameNotify.emit(value)

    @Property(str, notify=statusNotify)
    def status(self):
        return self._channel_data.status.value if self._channel_data and self._channel_data.status else ""

    @status.setter
    def status(self, value):
        if self._channel_data.status.value != value:
            # Convert string to enum, handling case insensitivity
            status_enum = Status(value.upper())
            self._channel_data.status = status_enum
            self.statusNotify.emit(value)


class DioEchoProxy(QObject):
    statusNotify = Signal(str)

    def __init__(self, status, parent=None):
        super().__init__(parent)
        self._status = status

    @Property(str, notify=statusNotify)
    def status(self):
        return self._status.value

    @status.setter
    def status(self, value):
        if self._status.value != value:
            # Convert string to enum, handling case insensitivity
            status_enum = Status(value.upper())
            self._status = status_enum
            self.statusNotify.emit(value)


class Pcie1762hProxy(QObject):
    def __init__(self, pcie_data, parent=None):
        super().__init__(parent)
        self._pcie_data = pcie_data
        self._do_channels = []
        self._di_channels = []

        self._do_echos = [DioEchoProxy(Status.NA) for i in range(16)]
        self._di_echos = [DioEchoProxy(Status.NA) for i in range(16)]

        if self._pcie_data:
            # sort channels by index
            sorted_do = sorted(self._pcie_data.do_channels, key=lambda c: c.index)
            sorted_di = sorted(self._pcie_data.di_channels, key=lambda c: c.index)

            for ch_data in sorted_do:
                self._do_channels.append(DioChannelProxy(ch_data, DioChannelType.DO, self))
            # for ch_data in sorted_di:
            #     self._di_channels.append(DioChannelProxy(ch_data, DioChannelType.DI, self))

    @Property('QVariant', constant=True)
    def doChannels(self):
        return self._do_channels

    # @Property('QVariant', constant=True)
    # def diChannels(self):
    #     return self._di_channels

    @Property('QVariant', constant=True)
    def doEchos(self):
        return self._do_echos

    @Property('QVariant', constant=True)
    def diEchos(self):
        return self._di_echos

    @Slot(int, str)
    def setDoChannelName(self, index, name):
        if self._pcie_data:
            channel = next((ch for ch in self._pcie_data.do_channels if ch.index == index), None)
            if channel:
                channel.name = name
                use_cases.pcie1726h_config.save(self._pcie_data)

    @Slot(int, str)
    def setDoChannelStatus(self, index, status):
        if self._pcie_data:
            channel = next((ch for ch in self._do_channels if ch.index == index), None)
            if channel:
                # Convert string to enum, handling case insensitivity
                channel.status = status
                use_cases.pcie1726h_config.save(self._pcie_data)

    @Slot()
    def reset(self):
        logger.info(f"reset")
        if self._pcie_data:
            for ch in self._do_channels:
                ch.status = "NA"

    @Slot()
    def test(self):
        logger.info(f"test")
        # TODO: Implement test logic with Pcie1762hPort
        pass
