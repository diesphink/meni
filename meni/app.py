from PySide6 import QtWidgets, QtCore
from meni.ui.windows.mainwindow import MainWindow
from meni.ui.windows.welcome import WelcomeWindow
from meni.model.model import JsonPickledMetadata
from meni.theme import *


class AppMeni(QtWidgets.QApplication):

    status = QtCore.Signal(str)
    filter_changed = QtCore.Signal()
    selected_files_changed = QtCore.Signal(list, object)
    theme_changed = QtCore.Signal(object)

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
        self.themes = {}

        for theme in [Nord(), Dracula(), Gruvbox()]:
            self.themes[theme.name] = theme

        theme = self.settings.value("theme", "Nord")
        if theme not in self.themes:
            theme = "Nord"
        self.set_theme(self.themes[theme])

        self.status.connect(print)

    def set_theme(self, theme):
        self.theme = theme

        self.setStyleSheet(
            f"""
                MainWindow, MainWindow * {{
                    background-color: {self.theme.main_background};
                    color: {self.theme.main_foreground};
                    selection-background-color: {self.theme.selection_background};
                    selection-color: {self.theme.selection_foreground};
                }}

                MainWindow::separator {{
                    background-color: rgba(0, 0, 0, 0.15);
                    width: 4px;
                    border: none;
                }}

                QPushButton#save:enabled, QPushButton#Ok:enabled {{
                    background-color: {self.theme.green_btn};
                    color: #000;
                }}

                QPushButton#cancel:enabled {{
                    background-color: {self.theme.red_btn};
                    color: #000;
                }}
                
                QLineEdit, QComboBox, QTextEdit, QPlainTextEdit {{
                    background-color: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(0, 0, 0, 0.3);
                }}

                QTableView QLineEdit, QTableView QComboBox {{
                    background-color: {self.theme.main_background};
                }}

                QTableView {{
                    gridline-color: rgba(0, 0, 0, 0.2);
                }}

                QMenuBar {{
                    border: 1px solid rgba(0, 0, 0, 0.2);
                }}

                QMenu {{
                    border: 1px solid rgba(0, 0, 0, 0.2);
                    background-color: {self.theme.main_background};
                    padding: 2px;
                }}
                
                DockTitleBar {{
                    background:rgba(0,0,0,0.1);
                }}

                DockTitleBar QLabel {{
                    background: transparent;
                }}

                DockTitleBar QPushButton {{
                    background: rgba(0, 0, 0, 0.1);
                    border: 0px solid white;
                    border-radius: 2px;
                }}

                DockTitleBar QPushButton::hover {{
                    background: rgba(0, 0, 0, 0.3);
                }}
                
                TagRow QLabel {{
                    background-color: {self.theme.tag_background};
                    color: {self.theme.tag_foreground};

                    opacity: 0.8;
                    font-size: 10px;
                    font-weight: bold;   

                    padding: 2px;
                    margin: 2px;
                    border-radius: 2px;
                }}

                BrowserDock {{
                    background: transparent;
                }}
                
                BrowserDock QTreeView::item {{
                    padding: 3px 0px;
                }}
                
                #empty {{
                    color: rgba(255,255,255,0.2);
                }}
                
                ViewerDock #title {{
                    font-size: 20px; font-weight: bold;text-decoration: underline;
                }}
                
                ViewerDock #path QLabel {{
                    font-size: 10px; opacity: 0.8
                }}
                
                ViewerDock #collection QLabel {{
                    font-size: 10px; opacity: 0.8
                }}
                
                ImportDialog TitleLabel {{
                    font-size: 15px;
                    font-weight: bold;
                    text-decoration: underline;
                }}
                
                DragAndDropTarget QLabel {{
                    background-color: rgba(255, 255, 255, 0.1); 
                    padding: 30px; 
                    border: 2px dashed rgba(255, 255, 255, 0.2); 
                    border-radius: 5px;
                    font-size: 17px;
                    text-align: center;
                }}
                
                WelcomeWindow, WelcomeWindow * {{
                    background-color: {self.theme.main_background}; 
                    color: {self.theme.main_foreground};
                    selection-background-color: {self.theme.selection_background};
                    selection-color: {self.theme.selection_foreground};
                }}
                
                WelcomeWindow QFrame {{
                    background-color: rgba(255, 255, 255, 0.01);
                }}    
                
                WelcomeWindow QLabel {{
                    background: transparent;
                    border: none;
                }}

                WelcomeWindow #path {{
                  border: 1px solid rgba(255,255,255, 0.2);
                  padding: 5px;
                  border-radius: 5px;
                  background-color: rgba(255,255,255, 0.1);
                }}

            """
        )
        self.theme_changed.emit(self.theme)
        self.settings.setValue("theme", theme.name)

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
