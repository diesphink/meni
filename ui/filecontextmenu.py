from PySide6 import QtWidgets, QtCore, QtGui
import qtawesome as qta


class FileContextMenu(QtWidgets.QMenu):
    def __init__(self, parent, files):
        super().__init__(parent)
        self.files = files
        self.app = QtCore.QCoreApplication.instance()
        remove_action = QtGui.QAction(
            f"Remove from library", self, icon=qta.icon("fa5s.minus-square", color=self.app.theme.icon_color), text="Remove from library"
        )
        remove_action.triggered.connect(self.remove_file)
        self.addAction(remove_action)

    def remove_file(self):
        dialog = QtWidgets.QMessageBox(self)
        dialog.setWindowTitle("Remove file")
        dialog.setIconPixmap(qta.icon("fa5.question-circle", color=self.app.theme.icon_color).pixmap(64, 64))

        deletion = self.files[0] if len(self.files) == 1 else f"{len(self.files)} files"
        dialog.setText(f"Are you sure you want to remove <b>{deletion}</b> from the library?<br><br>This will also remove the file(s) from disk.")
        dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        dialog.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

        if dialog.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            for file in self.files:
                self.app.metadata.remove_file(file)
                self.app.status.emit(f"Removed {file.name} from the library")
