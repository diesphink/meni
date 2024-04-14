from PySide6 import QtWidgets, QtCore, QtGui
from ui.common import DockTitleBar, IconLabel
from utils import tags_from_text

import qtawesome as qta


class PropertyRowWithApply(QtWidgets.QWidget):
    def __init__(self, parent, widget, apply_fn, has_apply_all=True):
        super().__init__(parent)

        self.app = QtCore.QCoreApplication.instance()
        self.has_apply_all = has_apply_all
        self.apply_fn = apply_fn

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        self.setLayout(self.layout)

        self.layout.addWidget(widget)

        self.apply = QtWidgets.QPushButton("", objectName="apply")
        self.apply.setIcon(qta.icon("fa5s.check", color=self.app.theme.icon_color))
        self.apply.clicked.connect(self.apply)
        self.apply.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.apply.setToolTip("<html>Apply to <b>last</b> selected file</html>")
        self.layout.addWidget(self.apply)

        if self.has_apply_all:
            self.apply_all = QtWidgets.QPushButton("", objectName="apply_all")
            self.apply_all.setIcon(qta.icon("fa5s.check-double", color=self.app.theme.icon_color))
            self.apply_all.clicked.connect(self.apply_all)
            self.apply_all.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.apply_all.setToolTip("<html>Apply to <b>all</b> selected files</html>")
            self.layout.addWidget(self.apply_all)

        self.app.selected_files_changed.connect(self.on_selected_file_changed)

    def apply(self):
        self.apply_fn()

    def apply_all(self):
        for file in self.app.selected_files:
            self.apply_fn(file)

    def on_selected_file_changed(self, files, last):
        if last:
            if self.has_apply_all:
                self.apply_all.setVisible(len(files) > 1)
                self.apply_all.setToolTip(f"<html>Apply to <b>all ({len(files)})</b> selected files</html>")

            self.apply.setToolTip(f"<html>Apply to last selected file, <b>{last}</b> (ENTER)</html>")
