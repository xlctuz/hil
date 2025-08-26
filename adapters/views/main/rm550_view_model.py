from PySide6.QtCore import QObject, Property, Signal, Slot
from core.usecases.toggle_rm550_output import ToggleRM550OutputUseCase



class RM550ViewModel(QObject):
    isEnabledChanged = Signal()
    currentResistanceChanged = Signal()

    def __init__(self, toggle_output_uc: ToggleRM550OutputUseCase, parent=None):
        super().__init__(parent)
        self._toggle_output_uc = toggle_output_uc

        self._is_enabled = False
        self._current_resistance = 0.0

    def update_data(self, resistance: float, is_enabled: bool):
        """This method is called by the parent ProjectViewModel to update the state."""
        self.isEnabled = is_enabled
        # Directly set the private member to avoid signal emission if value is the same
        if abs(self._current_resistance - resistance) > 1e-4:
            self._current_resistance = resistance
            self.currentResistanceChanged.emit()

    @Property(bool, notify=isEnabledChanged)
    def isEnabled(self):
        return self._is_enabled

    @isEnabled.setter
    def isEnabled(self, value):
        if self._is_enabled != value:
            self._is_enabled = value
            self.isEnabledChanged.emit()

    @Property(str, notify=currentResistanceChanged)
    def currentResistance(self):
        return f"{self._current_resistance:.3f}"

    @Slot(bool)
    def toggle_output(self, checked: bool):
        """Toggles the output of the RM550 device."""
        self._toggle_output_uc.execute(checked)
        # The actual state will be updated via the update_data callback from the monitoring task
