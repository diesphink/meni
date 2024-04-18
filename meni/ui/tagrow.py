from PySide6 import QtWidgets, QtCore
from meni.ui.flowlayout import FlowLayout


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
