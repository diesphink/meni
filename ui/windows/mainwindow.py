import os

from PySide6 import QtWidgets, QtCore, QtGui
from ui.filestable import FilesTable
from ui.searchinput import SearchInput
from ui.windows.importdialog import ImportDialog
from ui.menus.menusettings import MenuSettings
from ui.docks.viewer import ViewerDock
from ui.docks.filters import FiltersDock
from ui.docks.collectioninfo import CollectionDock
from ui.toolbars.maintoolbar import MainToolbar
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

                QMainWindow::separator {{
                    background-color: rgba(0, 0, 0, 0.15);
                    width: 4px;
                    border: none;
                }}

                QPushButton#save:enabled, QPushButton#Ok:enabled {{
                    background-color: {self.app.theme.green_btn};
                    color: #000;
                }}

                QPushButton#cancel:enabled {{
                    background-color: {self.app.theme.red_btn};
                    color: #000;
                }}
                
                QLineEdit, QComboBox {{
                    background-color: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(0, 0, 0, 0.3);
                }}

                QTableView QLineEdit, QTableView QComboBox {{
                    background-color: {self.app.theme.main_background};
                }}

            """
        )

        self.setWindowTitle("3D Library")
        self.setWindowFlags(QtCore.Qt.WindowType.Dialog)
        self.resize(self.app.settings.value("size", QtCore.QSize(270, 225)))
        self.move(self.app.settings.value("pos", QtCore.QPoint(50, 50)))

        self.toolbar = MainToolbar(self)
        self.addToolBar(self.toolbar)

        self.table = FilesTable()

        self.setCentralWidget(self.table)
        self.viewer = ViewerDock(self)
        self.filters = FiltersDock(self)
        self.collection_info = CollectionDock(self)

        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.viewer)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.filters)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.collection_info)

        self.app.status.connect(self.on_status)

        self.restoreState(self.app.settings.value("state"))

    def closeEvent(self, event):
        self.app.settings.setValue("size", self.size())
        self.app.settings.setValue("pos", self.pos())
        self.app.settings.setValue("state", self.saveState())
        event.accept()

    def on_status(self, message):
        self.statusBar().showMessage(message, 5000)
