from PySide6 import QtWidgets, QtCore, QtGui
from ui.common import DockTitleBar, IconLabel
from ui.propertyrowwithapply import PropertyRowWithApply
from utils import tags_from_text

import qtawesome as qta


class FilePropertiesDock(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super().__init__("File Properties", objectName="properties", parent=parent)

        self.setTitleBarWidget(DockTitleBar("File Properties", clicked=self.close))

        self.app = QtCore.QCoreApplication.instance()

        self.layout = QtWidgets.QFormLayout()

        self.empty = QtWidgets.QLabel("No file selected")
        self.empty.setAlignment(QtCore.Qt.AlignCenter)
        self.empty.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.empty.setStyleSheet("color: rgba(255,255,255,0.2);")
        self.layout.addRow(self.empty)

        # === Name
        self.name = QtWidgets.QLineEdit()
        self.name.returnPressed.connect(lambda: self.apply_file(name=self.name.text()))
        self.layout.addRow(
            "Name",
            PropertyRowWithApply(
                self,
                self.name,
                lambda: self.apply_file(name=self.name.text()),
                has_apply_all=False,
            ),
        )

        # === Collection
        self.collection = QtWidgets.QComboBox(self)
        self.collection.addItems([col.name for col in self.app.metadata.collections])
        self.collection_edit = QtWidgets.QLineEdit(self)
        self.collection.setLineEdit(self.collection_edit)
        self.collection_edit.setText("")
        self.collection_edit.returnPressed.connect(lambda: self.apply_file(collection=self.collection_edit.text()))

        self.layout.addRow(
            "Collection",
            PropertyRowWithApply(
                self,
                self.collection,
                lambda: self.apply_file(collection=self.collection_edit.text()),
            ),
        )

        # === Tags
        self.tags = QtWidgets.QLineEdit()
        self.tags.returnPressed.connect(lambda: self.apply_file(tags=tags_from_text(self.tags.text())))
        self.layout.addRow(
            "Tags",
            PropertyRowWithApply(
                self,
                self.tags,
                lambda: self.apply_file(tags=tags_from_text(self.tags.text())),
            ),
        )

        # Set layout to widget to dock
        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setWidget(widget)

        # Connect signals
        self.app.metadata.changed.connect(lambda: self.refresh(self.app.selected_file))
        self.app.selected_file_changed.connect(self.refresh)

        self.refresh(None)

    def refresh(self, file):
        self.layout.setRowVisible(0, file is None)
        for i in range(1, self.layout.rowCount()):
            self.layout.setRowVisible(i, file is not None)

        self.name.setText(file.name if file else "")
        self.collection_edit.setText(file.collection if file else "")
        self.tags.setText(", ".join(file.tags) if file else "")

    def apply_file(self, **kwargs):
        if self.app.selected_file:
            self.app.metadata.update_file(self.app.selected_file, **kwargs)
