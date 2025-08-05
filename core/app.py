from PySide6.QtCore import QObject


class App(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self._channel = Channel(0)

