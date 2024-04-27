from PySide6 import QtWidgets, QtCore
import qtawesome as qta


class QHLine(QtWidgets.QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class QVLine(QtWidgets.QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class DockTitleBar(QtWidgets.QWidget):
    def __init__(self, title, clicked=None, parent=None, closeable=True, draggable=True):
        super().__init__(parent)
        self.app = QtWidgets.QApplication.instance()

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(3, 3, 3, 3)
        self.layout.setSpacing(3)

        if draggable:
            drag_icon = QtWidgets.QLabel()
            drag_icon.setPixmap(qta.icon("fa5s.grip-vertical", color=self.app.theme.icon_color).pixmap(15))
            self.layout.addWidget(drag_icon)

        label = QtWidgets.QLabel(title)
        label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(label)

        if closeable:
            close = QtWidgets.QPushButton("", icon=qta.icon("fa5s.times", color=self.app.theme.icon_color), objectName="close", clicked=clicked)
            close.setFlat(True)
            close.setMouseTracking(True)
            self.layout.addWidget(close)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet(
            f"""
            DockTitleBar {{
                background:rgba(0,0,0,0.1);
            }}

            QLabel {{
                background: transparent;
            }}

            QPushButton {{
                background: rgba(0, 0, 0, 0.1);
                border: 0px solid white;
                border-radius: 2px;
            }}

            QPushButton::hover {{
                background: rgba(0, 0, 0, 0.3);
            }}
            """
        )


class IconLabel(QtWidgets.QWidget):

    HorizontalSpacing = 2

    def __init__(self, qta_id, text="", final_stretch=True, icon_size=16):
        super().__init__()

        self.app = QtWidgets.QApplication.instance()

        self.icon_size = QtCore.QSize(icon_size, icon_size)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.icon = QtWidgets.QLabel()
        self.text = QtWidgets.QLabel()

        self.setIcon(qta_id)
        self.setText(text)

        layout.addWidget(self.icon)
        layout.addSpacing(self.HorizontalSpacing)
        layout.addWidget(self.text)

        if final_stretch:
            layout.addStretch()

    def setText(self, text):
        self.text.setText(text)

    def setIcon(self, qta_id):
        self.icon.setPixmap(qta.icon(qta_id, color=self.app.theme.icon_color).pixmap(self.icon_size))
