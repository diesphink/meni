from PySide6 import QtWidgets, QtCore
from ui.common import DockTitleBar


class CollectionDock(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super().__init__("Collection", objectName="collection_info", parent=parent)

        self.app = QtCore.QCoreApplication.instance()

        self.setTitleBarWidget(DockTitleBar("Collection", clicked=self.close))

        self.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.setAllowedAreas(QtCore.Qt.DockWidgetArea.AllDockWidgetAreas)

        self.layout = QtWidgets.QVBoxLayout()
        # self.layout.setContentsMargins(0, 0, 0, 0)
        # self.layout.setSpacing(0)

        # Name
        self.layout.addWidget(QtWidgets.QLabel("Collection Name"))
        self.name = QtWidgets.QLineEdit()
        self.layout.addWidget(self.name)

        # Author
        self.layout.addWidget(QtWidgets.QLabel("Author"))
        self.author = QtWidgets.QLineEdit()
        self.layout.addWidget(self.author)

        # URL
        self.layout.addWidget(QtWidgets.QLabel("URL"))
        self.url = QtWidgets.QLineEdit()
        self.layout.addWidget(self.url)

        # # Attachments
        # self.layout.addWidget(QtWidgets.QLabel("Attachments"))
        # self.attachments = AttachmentsList()
        # self.layout.addWidget(self.attachments)

        # Notes
        self.layout.addWidget(QtWidgets.QLabel("Notes"))
        self.notes = QtWidgets.QTextEdit()
        self.layout.addWidget(self.notes)

        # Buttons
        self.save = QtWidgets.QPushButton("Save", objectName="save")
        self.cancel = QtWidgets.QPushButton("Cancel", objectName="cancel")
        self.buttons = QtWidgets.QHBoxLayout()
        self.buttons.addWidget(self.save)
        self.buttons.addWidget(self.cancel)
        self.layout.addLayout(self.buttons)

        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setWidget(widget)

        self.app.selected_file_changed.connect(self.refresh)
        self.app.metadata.changed.connect(lambda: self.refresh(self.app.selected_file))

        self.save.clicked.connect(self.save_collection)
        self.cancel.clicked.connect(lambda: self.refresh(self.app.selected_file))

    def save_collection(self):
        self.app.metadata.update_collection(
            self.app.selected_file.collection_obj,
            name=self.name.text(),
            author=self.author.text(),
            url=self.url.text(),
            notes=self.notes.toPlainText(),
        )

    def refresh(self, file):
        if file:
            collection = file.collection_obj

        if file and collection:
            self.name.setText(collection.name)
            self.author.setText(collection.author)
            self.url.setText(collection.url)
            self.notes.setText(collection.notes)
            # self.attachments.setAttachments(collection.attachments)
        else:
            self.name.setText("")
            self.author.setText("")
            self.url.setText("")
            self.notes.setText("")
            # self.attachments.setAttachments([])


# class AttachmentsList(QtWidgets.QLabel):
#     def __init__(self):
#         super().__init__()
#         self.setText("There are no attachments")
#         self.setStyleSheet("padding: 5px;text-align: center;")

#     def setAttachments(self, attachments):
#         if attachments:
#             self.setText("\n".join(attachments))
#         else:
#             self.setText("There are no attachments")
