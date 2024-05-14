from PySide6 import QtWidgets, QtCore
from meni.ui.flowlayout import FlowLayout


class TagRow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

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
            self.layout.addWidget(label)
