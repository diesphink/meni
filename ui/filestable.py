from PySide6 import QtWidgets, QtCore, QtGui
from ui.filecontextmenu import FileContextMenu
from ui.importdialog import ImportDialog
from utils import tags_from_text


class FilesTable(QtWidgets.QTableView):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setModel(TableModel())
        QtCore.QCoreApplication.instance().filter_changed.connect(self.on_filter_changed)
        self.selectionModel().selectionChanged.connect(self.on_selection_changed)
        header = self.horizontalHeader()

        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.setAcceptDrops(True)

    def contextMenuEvent(self, event):
        menu = FileContextMenu(self, self.model().files[self.selectionModel().currentIndex().row()])
        menu.popup(event.globalPos())

        return super().contextMenuEvent(event)

    def on_filter_changed(self):
        self.selectionModel().clearSelection()
        self.model().layoutChanged.emit()

    def on_selection_changed(self):
        app = QtCore.QCoreApplication.instance()
        if self.selectionModel().hasSelection():
            app.selected_file = self.model().files[self.selectionModel().currentIndex().row()]
        else:
            app.selected_file = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            files.append(url.toLocalFile())
        event.accept()
        ImportDialog(self, files).exec_()


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self):
        super(TableModel, self).__init__()
        self._files = QtCore.QCoreApplication.instance().metadata.files

    @property
    def files(self):
        app = QtCore.QCoreApplication.instance()

        filtered_files = self._files

        if app.tag_filters:
            filtered_files = [file for file in filtered_files if any(tag in app.tag_filters for tag in file.tags)]
        if app._search_filter:
            filtered_files = [file for file in filtered_files if app._search_filter.lower() in file.name.lower()]

        return filtered_files

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                if section == 0:
                    return "Name"
                elif section == 1:
                    return "Collection"
                elif section == 2:
                    return "Tags"
                elif section == 3:
                    return "Path"
            else:
                return section + 1
        return None

    def rowCount(self, index):
        return len(self.files)

    def columnCount(self, index):
        return 4

    def data(self, index, role):

        if role == QtCore.Qt.ItemDataRole.DisplayRole or role == QtCore.Qt.ItemDataRole.EditRole:
            if index.column() == 0:
                return self.files[index.row()].name
            elif index.column() == 1:
                return self.files[index.row()].collection.name
            elif index.column() == 2:
                return ", ".join(self.files[index.row()].tags)
            elif index.column() == 3:
                return self.files[index.row()].path

    def flags(self, index):
        flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        if index.column() == 0 or index.column() == 2:
            flags |= QtCore.Qt.ItemIsEditable
        return flags

    def validate(self, index, value):
        print(value)
        if index.column() == 0:
            return value.strip() != ""
        if index.column() == 2:
            return True
        return False

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            app = QtCore.QCoreApplication.instance()
            if index.column() == 0:
                if not self.validate(index, value):
                    return False
                app.metadata.update_file(self.files[index.row()], name=value)
            if index.column() == 2:
                app.metadata.update_file(self.files[index.row()], tags=tags_from_text(value))
            return True
