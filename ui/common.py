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
    def __init__(self, title, clicked=None, parent=None):
        super().__init__(parent)
        self.app = QtWidgets.QApplication.instance()

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(3, 3, 3, 3)
        self.layout.setSpacing(3)

        icon = QtWidgets.QLabel()
        icon.setPixmap(qta.icon("fa5s.grip-vertical", color=self.app.theme.icon_color).pixmap(15))
        self.layout.addWidget(icon)

        label = QtWidgets.QLabel(title)
        label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(label)

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
