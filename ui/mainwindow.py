import os

from PySide6 import QtWidgets, QtCore, QtGui
from ui.labelist import LabelList
from ui.filestable import FilesTable
from ui.viewer import Viewer
from ui.fileinfo import FileInfo
from ui.iconlabel import IconLabel
from ui.searchinput import SearchInput
from ui.importdialog import ImportDialog
import qtawesome as qta


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.app = QtCore.QCoreApplication.instance()

        self.setStyleSheet(
            f"""
                * {{
                    background-color: {self.app.theme.main_background};
                    color: {self.app.theme.main_foreground};
                    selection-background-color: {self.app.theme.selection_background};
                    selection-color: {self.app.theme.selection_foreground};
                }}
            """
        )

        self.setWindowTitle("3D Library")
        self.setWindowFlags(QtCore.Qt.WindowType.Dialog)
        self.resize(self.app.settings.value("size", QtCore.QSize(270, 225)))
        self.move(self.app.settings.value("pos", QtCore.QPoint(50, 50)))

        toolbar = self.addToolBar("Main")
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setIconSize(QtCore.QSize(16, 16))

        import_action = QtGui.QAction("Import", self, icon=qta.icon("fa5.plus-square", color=self.app.theme.icon_color), text="Import")
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(lambda: ImportDialog(self).exec())
        toolbar.addAction(import_action)

        toolbar.addSeparator()

        toolbar.addWidget(SearchInput())

        toolbar.addSeparator()
        settings_action = QtGui.QAction("Settings", self, icon=qta.icon("fa5s.cog", color=self.app.theme.icon_color), text="Settings")
        settings_action.triggered.connect(self.on_settings_button)
        toolbar.addAction(settings_action)

        self.labels = LabelList()
        self.table = FilesTable()
        self.viewer = Viewer()
        self.info = FileInfo()

        self.setCentralWidget(self.split(self.labels, self.split(self.table, self.vertical_stack(self.info, self.viewer))))

        self.app.metadata.changed.connect(self.table.model().layoutChanged)
        self.app.status.connect(self.on_status)

    def split(self, widget1, widget2, orientation=QtCore.Qt.Orientation.Horizontal):
        splitter = QtWidgets.QSplitter()
        splitter.setOrientation(orientation)
        splitter.addWidget(widget1)
        splitter.addWidget(widget2)

        return splitter

    def vertical_stack(self, *widgets):
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for widget in widgets:
            layout.addWidget(widget)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        return widget

    def closeEvent(self, event):
        self.app.settings.setValue("size", self.size())
        self.app.settings.setValue("pos", self.pos())
        event.accept()

    def model_changed(self):
        self.table.model().layoutChanged.emit()

    def on_status(self, message):
        self.statusBar().showMessage(message, 5000)

    def on_settings_button(self):
        from model.model import Stage, Collection, Local3DFile

        stage = Stage()
        stage.collection = Collection("Teste", notes="Observações", author="Someone", url="http://www.google.com")
        stage.tags = ["tag1", "tag2", "tag3"]

        stage.files.append(Local3DFile("/home/sphink/Downloads/111661.stl", stage.collection, name="Teste model with name"))
        stage.files.append(Local3DFile("/home/sphink/Downloads/Footer.stl", stage.collection))

        self.app.metadata.commit_stage(stage)
