from enum import Enum
from PySide6.QtCore import QObject, Property, Slot, Signal
from core.entities.pcie_1762h import Status
from core.usecases import UseCases
from core.logger import logger
import traceback


class DioChannelType(Enum):
    DO = 0
    DI = 1


class DioChannelViewModel(QObject):
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


class DioEchoViewModel(QObject):
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


class Pcie1762hViewModel(QObject):
    def __init__(self, usecases: UseCases, pcie_data, parent=None):
        super().__init__(parent)
        self.usecases = usecases
        self._pcie_data = pcie_data
        self._do_channels = []
        self._di_channels = []

        self._do_echos = [DioEchoViewModel(Status.NA) for i in range(16)]
        self._di_echos = [DioEchoViewModel(Status.NA) for i in range(16)]

        if self._pcie_data:
            # sort channels by index
            sorted_do = sorted(self._pcie_data.do_channels, key=lambda c: c.index)
            sorted_di = sorted(self._pcie_data.di_channels, key=lambda c: c.index)

            for ch_data in sorted_do:
                self._do_channels.append(DioChannelViewModel(ch_data, DioChannelType.DO, self))
            # for ch_data in sorted_di:
            #     self._di_channels.append(DioChannelViewModel(ch_data, DioChannelType.DI, self))

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
                self.usecases.save_pcie1762h_config(self._pcie_data)

    @Slot(int, str)
    def setDoChannelStatus(self, index, status):
        if self._pcie_data:
            channel = next((ch for ch in self._do_channels if ch.index == index), None)
            if channel:
                # Convert string to enum, handling case insensitivity
                channel.status = status
                self.usecases.save_pcie1762h_config(self._pcie_data)

    @Slot()
    def reset(self):
        logger.info(f"reset")
        if self._pcie_data:
            for ch in self._do_channels:
                ch.status = "NA"

    @Slot()
    def test(self):
        logger.info(f"test")
        if self._pcie_data:
            try:
                # Use the use case to test the PCIE-1762H device
                di_data = self.usecases.test_pcie_1762h(self._pcie_data)
                
                # Update DI echo channels with the returned data
                for i in range(16):
                    # Extract bit i from di_data
                    bit_value = (di_data >> i) & 1
                    status = Status.HIGH if bit_value else Status.LOW
                    
                    # Update the echo channel
                    if i < len(self._di_echos):
                        self._di_echos[i].status = status.value
                        
                logger.info(f"PCIE-1762H test completed, DI data: {di_data}")
            except Exception as e:
                logger.error(f"Error testing PCIE-1762H: {e}")
                # TODO: Handle error in UI
