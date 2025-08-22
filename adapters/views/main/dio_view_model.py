
from PySide6.QtCore import QObject, Property, Signal


class DioViewModel(QObject):
    def __init__(self, data, parent=None):
        super().__init__(parent)
