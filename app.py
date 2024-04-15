from PySide6 import QtWidgets, QtCore
from ui.windows.mainwindow import MainWindow
from ui.windows.welcome import WelcomeWindow
from model.model import JsonPickledMetadata
from theme import *


class App3dLibrary(QtWidgets.QApplication):

    status = QtCore.Signal(str)
    filter_changed = QtCore.Signal()
    selected_files_changed = QtCore.Signal(list, object)

    def __init__(self, sys_argv, library=None):
        super().__init__(sys_argv)

        self.setApplicationName("3D Library")

        self._library_command_line = library

        self.settings = QtCore.QSettings("3dlibrary", "3dlibrary")
        self.threadpool = QtCore.QThreadPool()
        self.threadpool.setMaxThreadCount(1)
        self.metadata = JsonPickledMetadata()

        self.main = None
        self.welcome = None
        self.tag_filters = []
        self._search_filter = None
        self._selected_files = []

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

    def is_tag_filtered(self, tag):
        return tag.name in self.tag_filters

    def toggle_tag_filter(self, tag):
        if tag.name in self.tag_filters:
            self.tag_filters.remove(tag.name)
        else:
            self.tag_filters.append(tag.name)

        self.filter_changed.emit()
