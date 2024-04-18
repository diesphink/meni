from PySide6 import QtWidgets, QtCore, QtGui
from meni.ui.windows.mainwindow import MainWindow
from meni.utils import pxmap_from_svg
import meni.rc_assets


class WelcomeWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # Attributes
        self.library_path = None

        self.app = QtCore.QCoreApplication.instance()

        # UI Components
        self.setStyleSheet(
            f"""
                           background-color: {self.app.theme.main_background}; 
                           color: {self.app.theme.main_foreground};
                           selection-background-color: {self.app.theme.selection_background};
                           selection-color: {self.app.theme.selection_foreground};
                           """
        )

        self.setWindowTitle("Welcome to Meni 3D Library")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(30, 15, 30, 15)

        # Logo (logo.svg)
        self.logo = QtWidgets.QLabel()
        self.logo.setPixmap(
            pxmap_from_svg(":/assets/logo.svg", color=self.app.theme.icon_color).scaled(
                120, 120, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            )
        )

        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.logo, 0)

        # Panel
        self.panel = QtWidgets.QFrame()
        self.panel.setFrameShape(QtWidgets.QFrame.Box)
        self.panel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.panel.setStyleSheet(
            """
                QFrame {
                        background-color: rgba(255, 255, 255, 0.01);
                        }            
                QLabel {
                    background: transparent;
                    border: none;
                    }
                                 """
        )
        self.panel.layout = QtWidgets.QVBoxLayout(self.panel)
        self.panel.layout.setContentsMargins(30, 15, 30, 30)
        self.panel.layout.setSpacing(15)
        self.layout.addWidget(self.panel, 1)

        # Text description
        self.description = QtWidgets.QLabel(
            """<strong>Welcome to Meni 3D Library</strong>
                <br><br>
                To get started with Meni, you'll need to designate a folder as your library. This folder will house your imported 3D models along with their associated metadata, including tags.
                <br><br>
                Please avoid selecting a folder that already contains your models; instead, import them into the library directly through the application.
                                    """,
        )
        self.description.setWordWrap(True)
        self.panel.layout.addWidget(self.description)

        # Path selection
        self.path = QtWidgets.QLabel(QtCore.QCoreApplication.instance().current_library)
        self.path.setStyleSheet(
            "border: 1px solid rgba(255,255,255, 0.2); padding: 5px; border-radius: 5px; background-color: rgba(255,255,255, 0.1); "
        )
        self.btn_browse = QtWidgets.QPushButton("Browse")
        self.btn_browse.clicked.connect(self.select_folder)

        self.rowLine = QtWidgets.QHBoxLayout()
        self.rowLine.addWidget(self.path, 1)
        self.rowLine.addWidget(self.btn_browse, 0)
        self.panel.layout.addLayout(self.rowLine)

        # Bottom buttons
        self.bottomButtons = QtWidgets.QHBoxLayout()
        self.bottomButtons.setContentsMargins(0, 15, 0, 0)
        self.layout.addLayout(self.bottomButtons, 0)

        self.btn_quit = QtWidgets.QPushButton("Quit")
        self.btn_quit.clicked.connect(self.close)
        self.bottomButtons.addWidget(self.btn_quit, 0)

        self.bottomButtons.addSpacerItem(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.btn_init = QtWidgets.QPushButton("Initialize Library")
        self.btn_init.setEnabled(QtCore.QCoreApplication.instance().current_library is not None)
        self.btn_init.setMinimumWidth(180)
        self.btn_init.setDefault(True)
        self.btn_init.clicked.connect(self.init)
        self.bottomButtons.addWidget(self.btn_init, 0)

    def select_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(None, "Select a folder")
        if folder:
            self.library_path = folder
            self.path.setText(folder)
            self.btn_init.setEnabled(True)

    def init(self):
        app = QtCore.QCoreApplication.instance()
        app.current_library = self.library_path
        app.show_main()
        self.hide()

    def close(self):
        QtCore.QCoreApplication.quit()
