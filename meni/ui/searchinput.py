from PySide6 import QtWidgets, QtCore, QtGui
from meni.ui.common import ThemedAction
import qtawesome as qta


class SearchInput(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.app = QtCore.QCoreApplication.instance()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.search = QtWidgets.QLineEdit()
        self.search.setPlaceholderText("Search")
        search_action = ThemedAction("Search", self, icon_id="fa5s.search", text="")
        self.search.addAction(search_action, QtWidgets.QLineEdit.LeadingPosition)
        self.layout.addWidget(self.search)

        self.clear_search = ThemedAction("Clear", self, icon_id="fa5s.backspace", text="")
        self.clear_search.triggered.connect(lambda: self.search.clear())
        self.clear_search.setEnabled(False)
        self.search.addAction(self.clear_search, QtWidgets.QLineEdit.TrailingPosition)

        self.search.textChanged.connect(self.on_text_changed)

    def on_text_changed(self, text):
        self.app.search_filter = text
        self.clear_search.setEnabled(bool(text))
