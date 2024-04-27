import os

from PySide6 import QtWidgets, QtCore, QtGui
from meni.ui.filestable import FilesTable
from meni.ui.searchinput import SearchInput
from meni.ui.windows.importdialog import ImportDialog
from meni.ui.menus.menusettings import MenuSettings
from meni.ui.docks.collectionproperties import CollectionPropertiesDock
from meni.ui.docks.fileproperties import FilePropertiesDock
from meni.ui.docks.viewer import ViewerDock
from meni.ui.docks.browser import BrowserDock
from meni.ui.common import DockTitleBar
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
                
                QLineEdit, QComboBox, QTextEdit, QPlainTextEdit {{
                    background-color: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(0, 0, 0, 0.3);
                }}

                QTableView QLineEdit, QTableView QComboBox {{
                    background-color: {self.app.theme.main_background};
                }}

                QTableView {{
                    gridline-color: rgba(0, 0, 0, 0.2);
                }}

                QMenuBar {{
                    border: 1px solid rgba(0, 0, 0, 0.2);
                }}

                QMenu {{
                    border: 1px solid rgba(0, 0, 0, 0.2);
                    background-color: {self.app.theme.main_background};
                    padding: 2px;
                }}
            """
        )

        self.setWindowTitle("Meni 3D Library")
        self.setWindowFlags(QtCore.Qt.WindowType.Dialog)
        self.resize(self.app.settings.value("size", QtCore.QSize(270, 225)))
        self.move(self.app.settings.value("pos", QtCore.QPoint(50, 50)))

        # Create docks
        self.viewer = ViewerDock(self)
        self.fileproperties = FilePropertiesDock(self)
        self.collectionproperties = CollectionPropertiesDock(self)
        self.browser = BrowserDock(self)

        # Add docks to main window
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.viewer)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.fileproperties)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.collectionproperties)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.browser)

        # Restore dock state
        self.restoreState(self.app.settings.value("state"))

        # Create File Menu
        file_menu = self.menuBar().addMenu("&File")
        file_menu.setShortcutEnabled(True)
        # File -> Import
        import_action = QtGui.QAction("Import", self, icon=qta.icon("fa5.plus-square", color=self.app.theme.icon_color), text="Import")
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(lambda: ImportDialog(self).exec())
        file_menu.addAction(import_action)
        # File -- Separator
        file_menu.addSeparator()
        # File -> Quit
        quit_action = QtGui.QAction("Quit", self, icon=qta.icon("fa5s.times", color=self.app.theme.icon_color), text="Quit")
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Create View Menu
        view_menu = self.menuBar().addMenu("&View")
        view_menu.setShortcutEnabled(True)
        # View -> Show Browser Dock
        dock_browser_action = QtGui.QAction("Show Browser Dock", self, checkable=True, checked=not self.browser.isHidden())
        dock_browser_action.triggered.connect(lambda: self.browser.setVisible(dock_browser_action.isChecked()))
        view_menu.addAction(dock_browser_action)
        # View -> Show Collection Properties Dock
        dock_collectionproperties_action = QtGui.QAction(
            "Show Collection Properties Dock", self, checkable=True, checked=not self.collectionproperties.isHidden()
        )
        dock_collectionproperties_action.triggered.connect(lambda: self.collectionproperties.setVisible(dock_collectionproperties_action.isChecked()))
        view_menu.addAction(dock_collectionproperties_action)
        # View -> Show File Properties Dock
        dock_fileproperties_action = QtGui.QAction("Show File Properties Dock", self, checkable=True, checked=not self.fileproperties.isHidden())
        dock_fileproperties_action.triggered.connect(lambda: self.fileproperties.setVisible(dock_fileproperties_action.isChecked()))
        view_menu.addAction(dock_fileproperties_action)
        # View -> Show Viewer Dock
        dock_viewer_action = QtGui.QAction("Show Viewer Dock", self, checkable=True, checked=not self.viewer.isHidden())
        dock_viewer_action.triggered.connect(lambda: self.viewer.setVisible(dock_viewer_action.isChecked()))
        view_menu.addAction(dock_viewer_action)

        # Create Settings Menu
        settings_menu = self.menuBar().addMenu("&Settings")
        settings_menu.setShortcutEnabled(True)
        # Settings -> Open Library Folder
        open_library_folder_action = QtGui.QAction(
            f"Open Library Folder...", self, icon=qta.icon("fa5s.folder-open", color=self.app.theme.icon_color), text="Open Library Folder..."
        )
        open_library_folder_action.triggered.connect(self.on_open_library_folder)
        settings_menu.addAction(open_library_folder_action)

        # Create Help Menu
        help_menu = self.menuBar().addMenu("&Help")
        help_menu.setShortcutEnabled(True)
        # Help -> About
        about_action = QtGui.QAction("About", self, icon=qta.icon("fa5s.info-circle", color=self.app.theme.icon_color), text="About")
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)

        self.table = FilesTable()
        main = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(DockTitleBar("Files", closeable=False, draggable=False))
        layout.addWidget(SearchInput())
        layout.addWidget(self.table)
        main.setLayout(layout)
        self.setCentralWidget(main)

        self.app.status.connect(self.on_status)

    def closeEvent(self, event):
        self.app.settings.setValue("size", self.size())
        self.app.settings.setValue("pos", self.pos())
        self.app.settings.setValue("state", self.saveState())
        event.accept()

    def on_status(self, message):
        self.statusBar().showMessage(message, 5000)

    def on_open_library_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(None, "Select a folder")
        if folder:
            self.app.current_library = folder
            self.app.metadata.changed.emit()

    def on_about(self):
        QtWidgets.QMessageBox.about(
            self,
            "About Meni",
            f"""
            <h1>Meni</h1>
            <p>Version: 0.1.0</p>
            """,
        )
