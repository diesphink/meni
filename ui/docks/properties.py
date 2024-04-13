from PySide6 import QtWidgets, QtCore, QtGui
from ui.common import DockTitleBar, IconLabel
from utils import tags_from_text

import qtawesome as qta


class PropertiesDock(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super().__init__("Properties", objectName="properties", parent=parent)

        self.app = QtCore.QCoreApplication.instance()

        self.setTitleBarWidget(DockTitleBar("Properties", clicked=self.close))

        self.layout = QtWidgets.QFormLayout()

        self.selected_files = IconLabel(text="No file selected", qta_id="fa5s.file", icon_size=12)
        self.selected_files.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)
        self.selected_files.setStyleSheet(
            """
            IconLabel {font-size: 10px; padding: 7px; background-color: rgba(255,255,255,0.03); margin: 0px; border-radius: 3px;}
            IconLabel QLabel {background-color: transparent; margin: 5px;}
            """
        )
        # self.layout.addRow(self.selected_files)

        # === Name
        self.name = QtWidgets.QLineEdit()
        self.name.returnPressed.connect(lambda: self.apply_file(name=self.name.text()))
        self.layout.addRow(
            "Name",
            WidgetWithApplyButtons(
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
            WidgetWithApplyButtons(
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
            WidgetWithApplyButtons(
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
        self.selected_files.setText(str(file) if file else "No file selected")

        for i in range(self.layout.rowCount()):
            self.layout.setRowVisible(i, file is not None)

        self.name.setText(file.name if file else "")
        self.collection_edit.setText(file.collection if file else "")
        self.tags.setText(", ".join(file.tags) if file else "")

    def apply_file(self, **kwargs):
        if self.app.selected_file:
            self.app.metadata.update_file(self.app.selected_file, **kwargs)

    def apply_file_all(self, **kwargs):
        if self.app.selected_file:
            self.app.metadata.update_file(self.app.selected_file, **kwargs)


class WidgetWithApplyButtons(QtWidgets.QWidget):
    def __init__(self, parent, widget, apply_fn, has_apply_all=True):
        super().__init__(parent)

        self.app = QtCore.QCoreApplication.instance()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        self.setLayout(self.layout)

        self.layout.addWidget(widget)

        self.apply = QtWidgets.QPushButton("", objectName="apply")
        self.apply.setIcon(qta.icon("fa5s.check", color=self.app.theme.icon_color))
        self.apply.clicked.connect(apply_fn)
        self.apply.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.apply.setToolTip("<html>Apply to <b>last</b> selected file</html>")
        self.layout.addWidget(self.apply)

        if has_apply_all:
            self.apply_all = QtWidgets.QPushButton("", objectName="apply_all")
            self.apply_all.setIcon(qta.icon("fa5s.check-double", color=self.app.theme.icon_color))
            self.apply_all.clicked.connect(apply_fn)
            self.apply_all.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.apply_all.setToolTip("<html>Apply to <b>all</b> selected files</html>")
            self.layout.addWidget(self.apply_all)
