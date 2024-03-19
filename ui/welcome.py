from PySide6 import QtWidgets, QtCore, QtGui
from ui.mainwindow import MainWindow


class WelcomeWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # Attributes
        self.library_path = None

        # UI Components

        self.setWindowTitle("Welcome to 3D Library")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(30, 15, 30, 15)

        # Title
        self.title = QtWidgets.QLabel("3D Library", alignment=QtCore.Qt.AlignCenter)
        self.title.setFont(QtGui.QFont("Sans", 30, QtGui.QFont.Bold))
        self.layout.addWidget(self.title, 0)

        # Panel
        self.panel = QtWidgets.QFrame()
        self.panel.setFrameShape(QtWidgets.QFrame.Box)
        self.panel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.panel.layout = QtWidgets.QVBoxLayout(self.panel)
        self.panel.layout.setContentsMargins(30, 15, 30, 30)
        self.panel.layout.setSpacing(15)
        self.layout.addWidget(self.panel, 1)

        # Text description
        self.description = QtWidgets.QLabel(
            """<strong>Welcome to 3D Library</strong>
                                    <br><br>
                                    3D Library needs a folder to use as your library. In this folder will be stored your 3D models after importing and the corresponding metadata, such as tags.
                                    <br><br>
                                    Do <strong>not</strong> select a folder already containing your models, you should import the models into the library through the application.
                                    """,
            alignment=QtCore.Qt.AlignCenter,
        )
        self.description.setWordWrap(True)
        self.description.setMinimumSize(300, 300)
        self.panel.layout.addWidget(self.description)

        # Path selection
        self.path = QtWidgets.QLabel(QtCore.QCoreApplication.instance().current_library)
        self.path.setStyleSheet("border: 1px solid #ccc; padding: 5px; border-radius: 5px;")
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
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select a folder")
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
