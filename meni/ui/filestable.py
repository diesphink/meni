from PySide6 import QtWidgets, QtCore, QtGui
from meni.ui.menus.filecontextmenu import FileContextMenu
from meni.ui.windows.importdialog import ImportDialog
from meni.utils import tags_from_text
import qtawesome as qta


class FilesTable(QtWidgets.QTableView):
    def __init__(self):
        super().__init__()
        self.app = QtCore.QCoreApplication.instance()
        self.delegate = PreviewDelegate()

        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setModel(TableModel())

        self.setItemDelegateForColumn(0, self.delegate)
        self.verticalHeader().setDefaultSectionSize(self.delegate.size)
        self.verticalHeader().hide()

        self.selectionModel().selectionChanged.connect(self.on_selection_changed)
        header = self.horizontalHeader()

        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.DragDrop)
        self.setDragDropOverwriteMode(False)
        self.setAcceptDrops(True)

        self.app.filter_changed.connect(self.on_filter_changed)
        self.app.metadata.changed.connect(self.model().layoutChanged.emit)

    def contextMenuEvent(self, event):
        files = [self.model().files[row.row()] for row in self.selectionModel().selectedRows()]
        if files:
            menu = FileContextMenu(self, files)
            menu.popup(event.globalPos())

        return super().contextMenuEvent(event)

    def on_filter_changed(self):
        self.selectionModel().clearSelection()
        self.model().layoutChanged.emit()

    def on_selection_changed(self):
        app = QtCore.QCoreApplication.instance()

        if self.selectionModel().hasSelection():
            app.selected_files = [self.model().files[row.row()] for row in self.selectionModel().selectedRows()]
        else:
            app.selected_files = None

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

    @property
    def size(self):
        return self.delegate.size

    @size.setter
    def size(self, value):
        self.delegate.size = value
        self.verticalHeader().setDefaultSectionSize(value)
        self.model().layoutChanged.emit()


class PreviewDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self):
        super().__init__()
        self.size = 50

    def paint(self, painter, option, index):

        # data is our preview object
        data = index.model().data(index, QtCore.Qt.DisplayRole)

        if data is None:
            return

        image = QtGui.QImage(data)

        scaled = image.scaled(
            self.size,
            self.size,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
        )
        # Position in the middle of the area.
        # x = CELL_PADDING + (width - scaled.width()) / 2
        # y = CELL_PADDING + (height - scaled.height()) / 2

        painter.drawImage(option.rect.x(), option.rect.y(), scaled)

    def sizeHint(self, option, index):
        # All items the same size.
        return QtCore.QSize(self.size, self.size)


THUMBNAIL, NAME, COLLECTION, TAGS, PATH = range(5)


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self):
        super(TableModel, self).__init__()
        self._files = QtCore.QCoreApplication.instance().metadata.files
        self.app = QtCore.QCoreApplication.instance()

    @property
    def files(self):
        app = QtCore.QCoreApplication.instance()

        filtered_files = self._files

        for filter in app.filters:
            filtered_files = [file for file in filtered_files if filter(file)]

        if app._search_filter:
            filtered_files = [file for file in filtered_files if app._search_filter.lower() in file.name.lower()]

        return filtered_files

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                if section == THUMBNAIL:
                    return ""
                elif section == NAME:
                    return "Name"
                elif section == COLLECTION:
                    return "Collection"
                elif section == TAGS:
                    return "Tags"
                elif section == PATH:
                    return "Path"
            else:
                return section + 1
        return None

    def rowCount(self, index):
        return len(self.files)

    def columnCount(self, index):
        return 5

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole or role == QtCore.Qt.ItemDataRole.EditRole:
            if index.column() == THUMBNAIL:
                return self.files[index.row()].thumbnail_file
            elif index.column() == NAME:
                return self.files[index.row()].name
            elif index.column() == COLLECTION:
                return self.files[index.row()].collection
            elif index.column() == TAGS:
                return ", ".join(self.files[index.row()].tags)
            elif index.column() == PATH:
                return self.files[index.row()].path

        elif role == QtCore.Qt.DecorationRole:
            if index.column() == COLLECTION:
                if self.files[index.row()].collection_obj is not None:
                    return qta.icon("fa5s.layer-group", color=self.app.theme.icon_color)
            elif index.column() == TAGS:
                if self.files[index.row()].tags:
                    return qta.icon("fa5s.tag", color=self.app.theme.icon_color)
            elif index.column() == PATH:
                return qta.icon("fa5s.file", color=self.app.theme.icon_color)

    def flags(self, index):
        flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled
        if index.column() == NAME or index.column() == COLLECTION or index.column() == TAGS:
            flags |= QtCore.Qt.ItemIsEditable
        return flags

    def validate(self, index, value):
        if index.column() == NAME:
            return value.strip() != ""
        if index.column() == COLLECTION:
            return True
        if index.column() == TAGS:
            return True
        return False

    def mimeData(self, indexes):

        rows = set(index.row() for index in indexes)
        urls = [QtCore.QUrl.fromLocalFile(self.files[row].absolute_path) for row in rows]

        mime_data = QtCore.QMimeData()
        mime_data.setUrls(urls)
        return mime_data

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            app = QtCore.QCoreApplication.instance()
            if index.column() == NAME:
                if not self.validate(index, value):
                    return False
                app.metadata.update_file(self.files[index.row()], name=value)
            if index.column() == COLLECTION:
                app.metadata.update_file(self.files[index.row()], collection=value)
            if index.column() == TAGS:
                app.metadata.update_file(self.files[index.row()], tags=tags_from_text(value))
            return True
