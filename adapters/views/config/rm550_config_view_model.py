from PySide6.QtCore import QObject, Property, Signal, Slot
from core.entities.rm550 import RM550
from core.usecases import UseCases


class RM550ConfigViewModel(QObject):
    portChanged = Signal()
    baudrateChanged = Signal()
    initialResistanceChanged = Signal()

    def __init__(self, usecases: UseCases, data: RM550, parent=None):
        super().__init__(parent)
        self._get_data_uc = usecases.get_rm550_config
        self._save_data_uc = usecases.save_rm550_config
        self._apply_resistance_uc = usecases.apply_rm550_resistance

        self._data = data
        # self._config = self._get_config_uc.execute()
        # if not self._config:
        #     # Create a default config if none exists
        #     self._config = RM550(id=1, port='COM3', baudrate=115200, initial_resistance=100.0)

    @Property(str, notify=portChanged)
    def port(self):
        return self._data.port if self._data else None

    @port.setter
    def port(self, value):
        if self._data.port != value:
            self._data.port = value
            self.portChanged.emit()

    @Property(int, notify=baudrateChanged)
    def baudrate(self):
        return self._data.baudrate

    @baudrate.setter
    def baudrate(self, value):
        if self._data.baudrate != value:
            self._data.baudrate = value
            self.baudrateChanged.emit()

    @Property(float, notify=initialResistanceChanged)
    def initialResistance(self):
        return self._data.initial_resistance

    @initialResistance.setter
    def initialResistance(self, value):
        if self._data.initial_resistance != value:
            self._data.initial_resistance = value
            self.initialResistanceChanged.emit()

    @Slot()
    def save_data(self):
        """Saves the current configuration to the database."""
        self._save_data_uc.execute(self._data)

    @Slot(float)
    def apply_resistance(self, resistance: float):
        """Applies the resistance value to the device."""
        self._apply_resistance_uc.execute(resistance)
        # Also update the initial resistance in the config object
        self.initialResistance = resistance
