from PySide6 import QtWidgets, QtCore, QtGui
from ui.searchinput import SearchInput
from ui.windows.importdialog import ImportDialog
from ui.menus.menusettings import MenuSettings

import qtawesome as qta


class MainToolbar(QtWidgets.QToolBar):
    def __init__(self, parent=None):
        super().__init__("Main", parent=parent)

        self.app = QtCore.QCoreApplication.instance()

        self.setObjectName("main_toolbar")
        self.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setMovable(False)
        self.setFloatable(False)
        self.setIconSize(QtCore.QSize(16, 16))

        import_action = QtGui.QAction("Import", self, icon=qta.icon("fa5.plus-square", color=self.app.theme.icon_color), text="Import")
        import_action.setShortcut("Ctrl+I")
        import_action.triggered.connect(lambda: ImportDialog(self).exec())
        self.addAction(import_action)

        self.addSeparator()

        self.addWidget(SearchInput())

        self.addSeparator()
        settings_action = QtGui.QAction("Settings", self, icon=qta.icon("fa5s.cog", color=self.app.theme.icon_color), text="Settings")
        settings_action.setMenu(MenuSettings(self))
        self.addAction(settings_action)
