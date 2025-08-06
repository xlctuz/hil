from PySide6.QtCore import QObject


class Project(QObject):
    def __init__(self, index, parent=None):
        super().__init__(parent)
        self._index = index;
