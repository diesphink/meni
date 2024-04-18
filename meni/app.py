from PySide6 import QtWidgets, QtCore
from meni.ui.windows.mainwindow import MainWindow
from meni.ui.windows.welcome import WelcomeWindow
from meni.model.model import JsonPickledMetadata
from meni.theme import *


class AppMeni(QtWidgets.QApplication):

    status = QtCore.Signal(str)
    filter_changed = QtCore.Signal()
    selected_files_changed = QtCore.Signal(list, object)

    def __init__(self, sys_argv, library=None):
        super().__init__(sys_argv)

        self.setApplicationName("Meni 3D Library")

        self._library_command_line = library

        self.settings = QtCore.QSettings("meni", "meni")
        # self.threadpool = QtCore.QThreadPool()
        # self.threadpool.setMaxThreadCount(1)
        self.metadata = JsonPickledMetadata()

        self.main = None
        self.welcome = None
        self._search_filter = None
        self._selected_files = []
        self.filters = []

        self.theme = Nord()
        # self.theme = Dracula()
        # self.theme = Gruvbox()

        self.status.connect(print)

    def startup(self):
        if self.current_library:
            self.show_main()
        else:
            self.show_welcome()

    def show_main(self):
        if not self.main:
            self.main = MainWindow()
        self.main.show()

    def show_welcome(self):
        if not self.welcome:
            self.welcome = WelcomeWindow()
        self.welcome.show()

    def add_filter(self, filter):
        self.filters.append(filter)

    @property
    def current_library(self):
        return self._library_command_line or self.settings.value("current_library")

    @current_library.setter
    def current_library(self, value):
        self.settings.setValue("current_library", value)
        self._library_command_line = None
        self.metadata.reload()

    @property
    def last_selected_file(self):
        if len(self._selected_files) > 0:
            return self._selected_files[-1]
        return None

    @property
    def selected_files(self):
        return self._selected_files

    @selected_files.setter
    def selected_files(self, list):
        self._selected_files = list
        self.selected_files_changed.emit(list, list[-1] if list else None)

    @property
    def search_filter(self):
        return self._search_filter

    @search_filter.setter
    def search_filter(self, value):
        self._search_filter = value
        self.filter_changed.emit()
