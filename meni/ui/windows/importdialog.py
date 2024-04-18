from PySide6 import QtWidgets, QtCore, QtGui
from meni.model.model import Local3DFile, Stage
from meni.ui.common import QHLine, QVLine
from meni.utils import tags_from_text
import os


class ImportDialog(QtWidgets.QDialog):
    def __init__(self, parent, files=None):
        super().__init__(parent)

        self.stage = Stage()
        self.app = QtCore.QCoreApplication.instance()

        self.setWindowTitle("Meni 3D Library - Import")

        hlayout = QtWidgets.QHBoxLayout()

        # Left panel
        self.left_panel = Panel("1. Add files", "Supported file format: STL. You can drag multiple files or a folder containing 3D models.")
        self.dndtarget = DragAndDropTarget()
        self.dndtarget.files_droped.connect(self.add_files)
        self.left_panel.add_widget(self.dndtarget)
        self.left_panel.add_widget(QtWidgets.QLabel("OR", alignment=QtCore.Qt.AlignmentFlag.AlignCenter))
        self.btn_browse_files = QtWidgets.QPushButton("Browse files...")
        self.btn_browse_files.clicked.connect(self.browse_files)
        self.left_panel.add_widget(self.btn_browse_files)

        hlayout.addWidget(self.left_panel)
        hlayout.addWidget(QVLine())

        # Middle panel
        self.middle_panel = Panel(
            "2. Rename the files",
            "Double-click to rename files as needed. You can always change the name later.",
        )
        self.file_list = AddedFilesTable()
        self.file_list.itemChanged.connect(self.on_edit)
        self.middle_panel.add_widget(self.file_list)

        hlayout.addWidget(self.middle_panel)
        hlayout.addWidget(QVLine())

        # Right panel
        self.right_panel = Panel(
            "3. Define collection and tags",
            "Define a collection and tags to apply to all imported files. You can modify them later.",
        )
        self.right_panel.add_widget(QtWidgets.QLabel("Collection name"))

        self.collection = QtWidgets.QComboBox(self)
        self.collection.addItems([col.name for col in self.app.metadata.collections])
        self.collection_edit = QtWidgets.QLineEdit(self)
        self.collection.setLineEdit(self.collection_edit)
        self.collection_edit.setText("")

        self.right_panel.add_widget(self.collection)
        self.right_panel.add_widget(QtWidgets.QLabel("Tags"))
        self.tags = QtWidgets.QLineEdit(self)
        self.right_panel.add_widget(self.tags)
        self.right_panel.layout.addStretch(1)

        hlayout.addWidget(self.right_panel)

        btns = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(btns)
        self.buttonBox.accepted.connect(self.on_OK)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(hlayout)
        self.layout.addWidget(QHLine())
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.add_files(files)

    def on_OK(self):
        self.stage.collection = self.collection.currentText()
        self.stage.tags = tags_from_text(self.tags.text())
        self.app.metadata.commit_stage(self.stage)
        self.accept()

    def add_files(self, files):
        if files:
            for file in files:
                self.add_file(file)

    def add_file(self, path):
        if os.path.isdir(path):
            for child in os.listdir(path):
                self.add_file(os.path.join(path, child))
        else:
            if path.lower().endswith(".stl"):
                file = Local3DFile(path, collection=None)
                self.stage.files.append(file)
                self.file_list.add_file(file)
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)

    def on_edit(self, item):
        file = self.stage.files[item.row()]
        if item.column() == 0:
            file.name = item.text()

    def browse_files(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setWindowTitle("Meni 3D Library")
        file_dialog.setDirectory(self.app.settings.value("last_path", QtCore.QDir.homePath()))
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("3D Files (*.stl)")
        file_dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        if file_dialog.exec_():
            paths = file_dialog.selectedFiles()
            for path in paths:
                self.app.settings.setValue("last_path", os.path.dirname(path))
                self.add_file(path)


class TitleLabel(QtWidgets.QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("font-size: 15px; font-weight: bold; text-decoration: underline;")


class Panel(QtWidgets.QWidget):
    def __init__(self, title, description):
        super().__init__()

        self.setMinimumSize(300, 300)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(TitleLabel(title))
        self.description = QtWidgets.QLabel(description, alignment=QtCore.Qt.AlignmentFlag.AlignTop)
        self.description.setWordWrap(True)
        self.description.setMinimumHeight(60)
        self.layout.addWidget(self.description)

    def add_widget(self, widget):
        self.layout.addWidget(widget)


class AddedFilesTable(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Name", ""])
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def add_file(self, file):
        row = self.rowCount()

        self.insertRow(row)
        self.setItem(row, 0, QtWidgets.QTableWidgetItem(file.name))
        self.setItem(row, 1, QtWidgets.QTableWidgetItem(file.path))

        # Make name editable
        item = self.item(row, 0)
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)

        # Disable path edition
        item = self.item(row, 1)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)


class DragAndDropTarget(QtWidgets.QWidget):

    files_droped = QtCore.Signal(list)

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)

        self.setStyleSheet(
            """
                           background-color: rgba(255, 255, 255, 0.1); 
                           padding: 30px; 
                           border: 2px dashed rgba(255, 255, 255, 0.2); 
                           border-radius: 5px;
                           font-size: 17px;
                           text-align: center;"""
        )
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QtWidgets.QLabel("Drag your model files here", alignment=QtCore.Qt.AlignmentFlag.AlignCenter))

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            files.append(url.toLocalFile())
        event.accept()
        self.files_droped.emit(files)
