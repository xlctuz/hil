from PySide6.QtCore import QObject, Property

from .channel import Channel


class App(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._channels = [Channel(0), Channel(1), Channel(2)]

    @Property(list, constant=True)
    def channels(self):
        return self._channels

