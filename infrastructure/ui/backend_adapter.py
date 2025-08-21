from PySide6.QtCore import QObject, Property
from infrastructure.ui.main_view_model import MainViewModel
from infrastructure.ui.config_view_model import ConfigViewModel


class BackendAdapter(QObject):
    def __init__(self, main_view_model: MainViewModel, config_view_model: ConfigViewModel, parent=None):
        super().__init__(parent)
        self._main_view_model = main_view_model
        self._config_view_model = config_view_model

    @Property(QObject, constant=True)
    def mainViewModel(self):
        return self._main_view_model

    @Property(QObject, constant=True)
    def configViewModel(self):
        return self._config_view_model