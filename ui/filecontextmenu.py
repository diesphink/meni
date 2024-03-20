from PySide6 import QtWidgets, QtCore, QtGui


class FileContextMenu(QtWidgets.QMenu):
    def __init__(self, parent, file):
        super().__init__(parent)
        self.file = file
        self.addAction("Open", self.open_file)
        self.addAction("Delete", self.delete_file)

    def open_file(self):
        app = QtCore.QCoreApplication.instance()
        app.status.emit(self.file)

    def delete_file(self):
        app = QtCore.QCoreApplication.instance()
        app.status.emit(self.file)
