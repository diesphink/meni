from PySide6 import QtWidgets, QtCore, QtGui
from meni.ui.common import ThemedAction
import qtawesome as qta


class MenuSettings(QtWidgets.QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.app = QtCore.QCoreApplication.instance()
        open_library_folder_action = ThemedAction(f"Open Library Folder...", self, icon_id="fa5s.folder-open", text="Open Library Folder...")
        open_library_folder_action.triggered.connect(self.on_open_library_folder)
        self.addAction(open_library_folder_action)

    def on_open_library_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(None, "Select a folder")
        if folder:
            self.app.current_library = folder
            self.app.metadata.changed.emit()
