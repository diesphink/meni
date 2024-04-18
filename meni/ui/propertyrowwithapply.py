from PySide6 import QtWidgets, QtCore, QtGui
from meni.ui.common import DockTitleBar, IconLabel
from meni.utils import tags_from_text

import qtawesome as qta


class PropertyRowWithApply(QtWidgets.QWidget):
    def __init__(self, parent, widget, apply_dict_fn, has_apply_all=True):
        super().__init__(parent)

        self.app = QtCore.QCoreApplication.instance()
        self.has_apply_all = has_apply_all
        self.apply_dict_fn = apply_dict_fn

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        self.setLayout(self.layout)

        self.layout.addWidget(widget)

        self.btn_apply = QtWidgets.QPushButton("", objectName="apply")
        self.btn_apply.setIcon(qta.icon("fa5s.check", color=self.app.theme.icon_color))
        self.btn_apply.clicked.connect(self.apply_last)
        self.btn_apply.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.btn_apply.setToolTip("<html>Apply to <b>last</b> selected file</html>")
        self.layout.addWidget(self.btn_apply)

        if self.has_apply_all:
            self.btn_apply_all = QtWidgets.QPushButton("", objectName="apply_all")
            self.btn_apply_all.setIcon(qta.icon("fa5s.check-double", color=self.app.theme.icon_color))
            self.btn_apply_all.clicked.connect(self.apply_all)
            self.btn_apply_all.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            self.btn_apply_all.setToolTip("<html>Apply to <b>all</b> selected files</html>")
            self.layout.addWidget(self.btn_apply_all)

        self.app.selected_files_changed.connect(self.on_selected_file_changed)

    def apply_last(self):
        self.apply(self.app.last_selected_file, **self.apply_dict_fn())

    def apply_all(self):
        args = self.apply_dict_fn()
        for file in self.app.selected_files:
            self.apply(file, **args)

    def apply(self, file, **kwargs):
        pass

    def on_selected_file_changed(self, files, last):
        if last:
            if self.has_apply_all:
                self.btn_apply_all.setVisible(len(files) > 1)
                self.btn_apply_all.setToolTip(f"<html>Apply to <b>all ({len(files)})</b> selected files</html>")

            self.btn_apply.setToolTip(f"<html>Apply to last selected file, <b>{last}</b> (ENTER)</html>")


class FilePropertyRowWithApply(PropertyRowWithApply):
    def __init__(self, parent, widget, apply_dict_fn, has_apply_all=True):
        super().__init__(parent, widget, apply_dict_fn, has_apply_all)

        self.apply_dict_fn = apply_dict_fn

    def apply(self, file, **kwargs):
        if file:
            self.app.metadata.update_file(file, **kwargs)


class CollectionPropertyRowWithApply(PropertyRowWithApply):
    def __init__(self, parent, widget, apply_dict_fn, has_apply_all=True):
        super().__init__(parent, widget, apply_dict_fn, has_apply_all)

        self.apply_dict_fn = apply_dict_fn

    def apply(self, file, **kwargs):
        if file and file.collection_obj:
            self.app.metadata.update_collection(file.collection_obj, **kwargs)
