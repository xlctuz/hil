from PySide6.QtCore import QObject


class App(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._channels = [Channel(0), Channel(1), Channel(2)]


