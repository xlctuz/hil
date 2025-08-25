from PySide6.QtCore import QObject, Property, Slot, Signal
from core.usecases import UseCases
from core.logger import logger


class Pci1720uChannelConfigViewModel(QObject):
    nameChanged = Signal()
    voltageChanged = Signal()

    def __init__(self, channel_data, parent=None):
        super().__init__(parent)
        self._channel_data = channel_data

    @Property(str, notify=nameChanged)
    def name(self):
        return self._channel_data.name if self._channel_data else ""

    @name.setter
    def name(self, value):
        if self._channel_data and self._channel_data.name != value:
            self._channel_data.name = value
            self.nameChanged.emit()

    @Property(float, notify=voltageChanged)
    def voltage(self):
        return self._channel_data.voltage if self._channel_data and self._channel_data.voltage is not None else 0.0

    @voltage.setter
    def voltage(self, value):
        if self._channel_data and self._channel_data.voltage != value:
            self._channel_data.voltage = value
            self.voltageChanged.emit()


class Pci1720uConfigViewModel(QObject):
    channelsChanged = Signal()

    def __init__(self, usecases: UseCases, pci1720u_data, parent=None):
        super().__init__(parent)
        self.usecases = usecases
        self._pci1720u_data = pci1720u_data
        self._channels = []
        if self._pci1720u_data:
            sorted_channels = sorted(self._pci1720u_data.channels, key=lambda c: c.index)
            self._channels = [Pci1720uChannelConfigViewModel(ch) for ch in sorted_channels]

    @Property('QVariant', notify=channelsChanged)
    def channels(self):
        return self._channels

    @Slot(int, str)
    def setChannelName(self, index, name):
        if self._pci1720u_data and 0 <= index < len(self.channels):
            self._channels[index].name = name
            self.usecases.save_pci1720u_config(self._pci1720u_data)

    @Slot(int, float)
    def setChannelVoltage(self, index, voltage):
        if self._pci1720u_data and 0 <= index < len(self.channels):
            self._channels[index].voltage = voltage
            self.usecases.save_pci1720u_config(self._pci1720u_data)

    @Slot()
    def test(self):
        logger.info("Testing PCI-1720U")
        if self._pci1720u_data:
            for channel_vm in self._channels:
                if channel_vm.name and channel_vm.voltage is not None:
                    try:
                        self.usecases.set_pci1720u_voltage(
                            self._pci1720u_data,
                            channel_vm._channel_data.index,
                            channel_vm.voltage
                        )
                    except Exception as e:
                        logger.error(f"Error testing PCI-1720U channel {channel_vm._channel_data.index}: {e}")
                        # Optionally, emit a signal to show the error in the UI
