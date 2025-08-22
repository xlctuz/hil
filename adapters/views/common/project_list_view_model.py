from PySide6.QtCore import QObject, Property, Slot, QAbstractListModel, QModelIndex, Qt, Signal, QThread, QTimer


class ProjectListViewModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    CheckedRole = Qt.UserRole + 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self._projects = []

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._projects)):
            return None
        project = self._projects[index.row()]
        if role == self.NameRole:
            return project.name
        if role == self.CheckedRole:
            return getattr(project, 'checked', False)
        return None

    def rowCount(self, parent=QModelIndex()):
        return len(self._projects)

    def roleNames(self):
        return {
            self.NameRole: b'name',
            self.CheckedRole: b'checked'
        }

    def set_projects(self, projects):
        self.beginResetModel()
        self._projects = projects
        # Add checked attribute for UI state
        for p in self._projects:
            p.checked = False
        self.endResetModel()

    def get_project(self, row):
        if 0 <= row < len(self._projects):
            return self._projects[row]
        return None

    def set_checked(self, row, checked=True):
        if 0 <= row < len(self._projects):
            # Uncheck others
            for i, p in enumerate(self._projects):
                if i != row and getattr(p, 'checked', False):
                    p.checked = False
                    self.dataChanged.emit(self.index(i, 0), self.index(i, 0), [self.CheckedRole])

            # Check selected
            project = self._projects[row]
            project.checked = checked
            self.dataChanged.emit(self.index(row, 0), self.index(row, 0), [self.CheckedRole])