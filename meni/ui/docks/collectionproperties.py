from PySide6 import QtWidgets, QtCore, QtGui
from meni.ui.common import DockTitleBar, IconLabel
from meni.ui.propertyrowwithapply import CollectionPropertyRowWithApply
from meni.utils import tags_from_text

import qtawesome as qta


class CollectionPropertiesDock(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super().__init__("Collection Properties", objectName="properties", parent=parent)

        self.app = QtCore.QCoreApplication.instance()

        self.setTitleBarWidget(DockTitleBar("Collection Properties", clicked=self.close))

        self.layout = QtWidgets.QFormLayout()

        self.empty = QtWidgets.QLabel("No collection selected")
        self.empty.setAlignment(QtCore.Qt.AlignCenter)
        self.empty.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.empty.setStyleSheet("color: rgba(255,255,255,0.2);")
        self.layout.addRow(self.empty)

        # === Name
        self.col_name = QtWidgets.QLineEdit()
        self.col_name.returnPressed.connect(lambda: self.apply_collection(name=self.col_name.text()))
        row = self.layout.addRow(
            "Name",
            CollectionPropertyRowWithApply(
                self,
                self.col_name,
                lambda: dict(name=self.col_name.text()),
                has_apply_all=False,
            ),
        )

        # === Author
        self.col_author = QtWidgets.QLineEdit()
        self.col_author.returnPressed.connect(lambda: self.apply_collection(author=self.col_author.text()))
        self.layout.addRow(
            "Author",
            CollectionPropertyRowWithApply(
                self,
                self.col_author,
                lambda: dict(author=self.col_author.text()),
            ),
        )

        # === URL
        self.col_url = QtWidgets.QLineEdit()
        self.col_url.returnPressed.connect(lambda: self.apply_collection(url=self.col_url.text()))
        self.layout.addRow(
            "URL",
            CollectionPropertyRowWithApply(
                self,
                self.col_url,
                lambda: dict(url=self.col_url.text()),
            ),
        )

        # === Notes
        self.col_notes = QtWidgets.QPlainTextEdit()
        self.layout.addRow(
            "Notes",
            CollectionPropertyRowWithApply(
                self,
                self.col_notes,
                lambda: dict(notes=self.col_notes.toPlainText()),
            ),
        )

        # Set layout to widget to dock
        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setWidget(widget)

        # Connect signals
        self.app.metadata.changed.connect(lambda: self.refresh([], self.app.last_selected_file))
        self.app.selected_files_changed.connect(self.refresh)

        self.refresh([], None)

    def refresh(self, files, last):
        collection = last and last.collection_obj
        if collection is not None:
            self.col_name.setText(collection.name)
            self.col_author.setText(collection.author)
            self.col_url.setText(collection.url)
            self.col_notes.setPlainText(collection.notes)

        self.layout.setRowVisible(0, collection is None)
        for i in range(1, self.layout.rowCount()):
            self.layout.setRowVisible(i, collection is not None)

    def apply_collection(self, **kwargs):
        if self.app.last_selected_file and self.app.last_selected_file.collection_obj:
            self.app.metadata.update_collection(self.app.last_selected_file.collection_obj, **kwargs)
