from enum import Enum
from PySide6.QtCore import QObject, Property, Slot, QAbstractListModel, QModelIndex, Qt, Signal, QThread, QTimer
from core.pcie_1762h_controller import Pcie_1762h, Pcie_1762h_do_channel, Pcie_1762h_di_channel, Status
from core.db import Session
from sqlalchemy.orm import sessionmaker, joinedload
from common.logger import logger

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
        if self._channel_data.name.value != value:
            self._channel_data.name.value = value
            self.nameNotify.emit(value)

    @Property(str, notify=statusNotify)
    def status(self):
        return self._channel_data.status.value if self._channel_data and self._channel_data.status else ""

    @status.setter
    def status(self, value):
        if self._channel_data.status != value:
            self._channel_data.status = value
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
        if self._status != value:
            self._status = value
            self.statusNotify.emit(value)


class Pcie1762hProxy(QObject):
    def __init__(self, pcie_data, parent=None):
        super().__init__(parent)
        logger.info(f"set pcie data {pcie_data}")
        self._pcie_data = pcie_data
        self._do_channels = []
        self._di_channels = []

        self._do_echos = [DioEchoProxy(Status.NA) for i in range(16)]
        self._di_echos = [DioEchoProxy(Status.LOW) for i in range(16)]

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

    @Property('QVariant', constant=True)
    def doEchos(self):
        return self._do_echos

    @Property('QVariant', constant=True)
    def diEchos(self):
        return self._di_echos

    @Slot(int, str)
    def setDoChannelName(self, index, name):
        session = Session()
        try:
            pcie = session.merge(self._pcie_data)
            channel = next((ch for ch in pcie.do_channels if ch.index == index), None)
            if channel:
                channel.name = name
                session.commit()
                self._pcie_data.do_channels[index].name = name
        finally:
            session.close()

    @Slot(int, str)
    def setDoChannelStatus(self, index, status):
        session = Session()
        try:
            pcie = session.merge(self._pcie_data)
            channel = next((ch for ch in pcie.do_channels if ch.index == index), None)
            if channel:
                channel.status = Status[status.upper()]
                session.commit()
                self._pcie_data.do_channels[index].status = Status[status.upper()]
        finally:
            session.close()

    @Slot()
    def reset(self):
        logger.info('pcie1762h reset')
        session = Session()
        try:
            session.merge(self._pcie_data)

            for ch in self._do_channels:
                ch.status = Status.NA

            session.commit()

        finally:
            session.close()

    @Slot()
    def test(self):
        logger.info('pcie1762h test')
        try:
            result = self._pcie_data.run_test()
            print(f"DO test result: {result}")

            for k in range(16):
                i = k // 8
                j = k % 8

                status = Status.HIGH if (result[i] & (1 << j) ) != 0 else Status.LOW
                self._do_echos[k].status = status
                logger.info(f"do echo {k} changed to {status}")

            di_status = self._pcie_data.get_di()
            print(f"DI status: {di_status}")

            for k in range(16):
                i = k // 8
                j = k % 8
                status = Status.HIGH if (di_status[i] & (1 << j) ) != 0 else Status.LOW
                self._di_echos[k].status = status
                logger.info(f"di echo {k} changed to {status}")

        except Exception as e:
            print(f"Error testing PCIE-1762H: {e}")
