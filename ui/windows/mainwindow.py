import os

from PySide6 import QtWidgets, QtCore, QtGui
from ui.filestable import FilesTable
from ui.searchinput import SearchInput
from ui.importdialog import ImportDialog
from ui.menusettings import MenuSettings
from ui.docks.viewer import ViewerDock
from ui.docks.filters import FiltersDock
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
        toolbar.setObjectName("main_toolbar")
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
        settings_action.setMenu(MenuSettings(self))
        toolbar.addAction(settings_action)

        self.table = FilesTable()

        self.setCentralWidget(self.table)
        self.viewer = ViewerDock(None)
        self.filters = FiltersDock(None)

        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.viewer)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.filters)

        self.app.metadata.changed.connect(self.table.model().layoutChanged)
        self.app.status.connect(self.on_status)

        self.restoreState(self.app.settings.value("state"))

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
        self.app.settings.setValue("state", self.saveState())
        event.accept()

    def model_changed(self):
        self.table.model().layoutChanged.emit()

    def on_status(self, message):
        self.statusBar().showMessage(message, 5000)
