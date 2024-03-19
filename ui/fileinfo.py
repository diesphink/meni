from PySide6 import QtWidgets, QtCore
from ui.flowlayout import FlowLayout
from utils import horizontal_layout

import qtawesome as qta


class FileInfo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.app = QtCore.QCoreApplication.instance()

        # self.setStyleSheet("background-color: #282828; color: #ebdbb2;")
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAutoFillBackground(True)

        self.layout = QtWidgets.QVBoxLayout()
        # self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.title = QtWidgets.QLabel()
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;text-decoration: underline;")
        self.title.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.layout.addWidget(self.title)

        self.path = QtWidgets.QLabel()
        self.path.setStyleSheet("font-size: 10px; opacity: 0.8")
        self.layout.addWidget(self.path)

        self.tagrow = TagRow()
        self.tagrow.setContentsMargins(0, 10, 0, 0)
        self.layout.addWidget(self.tagrow)

        self.tags = QtWidgets.QLabel()
        self.layout.addWidget(self.tags)

        app = QtCore.QCoreApplication.instance()
        app.selected_file_changed.connect(self.on_selected_file_changed)
        app.metadata.changed.connect(lambda: self.on_selected_file_changed(app.selected_file))

    def on_selected_file_changed(self, file):
        if file:
            self.title.setText(file.title)
            self.path.setText(file.path)
            self.tagrow.tags = file.tags


class TagRow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.app = QtCore.QCoreApplication.instance()

        self._tags = None

        self.layout = FlowLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout
        self.setLayout(self.layout)

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = tags
        self.build_tags()

    def build_tags(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for tag in self._tags:
            label = QtWidgets.QLabel(tag)
            label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            label.setStyleSheet(
                f"""
                background-color: {self.app.theme.tag_background};
                color: {self.app.theme.tag_foreground};

                opacity: 0.8;
                font-size: 10px;
                font-weight: bold;   

                padding: 2px;
                margin: 2px;
                border-radius: 2px;
                """
            )
            self.layout.addWidget(label)
