from PySide6 import QtWidgets, QtCore, QtGui
import qtawesome as qta


class LabelList(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: transparent;")

        self.setMaximumWidth(200)
        self.app = QtCore.QCoreApplication.instance()

        self.list = QtWidgets.QListWidget()
        self.list.clicked.connect(self.on_click)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.list)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.populate_list()
        self.app.metadata.changed.connect(self.populate_list)

    def populate_list(self):

        self.list.clear()

        for tag in sorted(self.app.metadata.tags, key=lambda x: x.quantity, reverse=True):
            list_item = TagListItem(tag)
            item = QtWidgets.QListWidgetItem()
            # Set size hint
            item.setSizeHint(list_item.sizeHint())
            item.tag = tag
            # Add QListWidgetItem into QListWidget
            self.list.addItem(item)
            self.list.setItemWidget(item, list_item)

    def on_click(self, index):
        app = QtCore.QCoreApplication.instance()

        item = self.list.currentItem()
        tag = item.tag

        app.toggle_tag_filter(tag)
        self.populate_list()


class TagListItem(QtWidgets.QWidget):
    def __init__(self, tag):
        super().__init__()

        self.tag = tag
        self.app = QtCore.QCoreApplication.instance()

        highlight = self.app.is_tag_filtered(tag)

        self.setStyleSheet(
            f"""
                           TagListItem {{
                               background: {'rgba(0,0,0,0.3)' if highlight else 'none'}; 
                               border-radius: 5px;
                               margin: 2px;
                            }}"""
        )
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

        icon = QtWidgets.QLabel()
        icon.setPixmap(
            qta.icon("fa.tag", color=self.app.theme.icon_color if not highlight else self.app.theme.main_background).pixmap(QtCore.QSize(16, 16))
        )

        layout.addWidget(icon)
        layout.setSpacing(2)
        layout.addWidget(QtWidgets.QLabel(tag.name))

        layout.addStretch()

        qtd_label = QtWidgets.QLabel(str(tag.quantity))
        qtd_label.setStyleSheet(
            f"""
            background: {self.app.theme.tag_background if not highlight else self.app.theme.main_background};
            color: {self.app.theme.tag_foreground if not highlight else self.app.theme.tag_background};
            padding: 2px;
            border-radius: 4px;
            font-size: 9px;
            font-weight: bold;
            """
        )
        qtd_label.setStyleSheet(
            f"""
            """
        )

        layout.addWidget(qtd_label)
