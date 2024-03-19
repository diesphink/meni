from PySide6 import QtWidgets, QtCore, QtGui


class FilesTable(QtWidgets.QTableView):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setModel(TableModel())
        QtCore.QCoreApplication.instance().filter_changed.connect(self.on_filter_changed)
        self.selectionModel().selectionChanged.connect(self.on_selection_changed)
        header = self.horizontalHeader()

        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

    def on_filter_changed(self):
        self.model().layoutChanged.emit()

    def on_selection_changed(self):
        app = QtCore.QCoreApplication.instance()
        app.selected_file = self.model().files[self.selectionModel().currentIndex().row()]


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self):
        super(TableModel, self).__init__()
        self._files = QtCore.QCoreApplication.instance().metadata.files

    def data(self, index, role):

        if role == QtCore.Qt.ItemDataRole.DisplayRole or role == QtCore.Qt.ItemDataRole.EditRole:
            if index.column() == 0:
                return self.files[index.row()].title
            elif index.column() == 1:
                return ", ".join(self.files[index.row()].tags)
            elif index.column() == 2:
                return self.files[index.row()].path

    @property
    def files(self):
        app = QtCore.QCoreApplication.instance()

        filtered_files = self._files

        if app.tag_filters:
            filtered_files = [file for file in filtered_files if any(tag in app.tag_filters for tag in file.tags)]
        if app._search_filter:
            filtered_files = [file for file in filtered_files if app._search_filter.lower() in file.title.lower()]

        return filtered_files

    def rowCount(self, index):
        return len(self.files)

    def columnCount(self, index):
        return 3

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                if section == 0:
                    return "Title"
                elif section == 1:
                    return "Tags"
                elif section == 2:
                    return "Path"
            else:
                return section + 1
        return None

    def flags(self, index):
        flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        if index.column() == 0 or index.column() == 1:
            flags |= QtCore.Qt.ItemIsEditable
        return flags

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            app = QtCore.QCoreApplication.instance()
            if index.column() == 0:
                app.metadata.update_file(self.files[index.row()], title=value)
            if index.column() == 1:
                app.metadata.update_file(self.files[index.row()], tags=[tag.strip() for tag in value.split(", ")])
            return True
