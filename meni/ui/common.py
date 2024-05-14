from PySide6 import QtWidgets, QtCore, QtGui
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
            self.layout.addWidget(ThemedIcon("fa5s.grip-vertical", size=15))

        label = QtWidgets.QLabel(title)
        label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(label)

        if closeable:
            close = ThemedQPushButton(icon_id="fa5s.times", objectName="close", clicked=clicked)
            close.setFlat(True)
            close.setMouseTracking(True)
            self.layout.addWidget(close)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground, True)


class IconLabel(QtWidgets.QWidget):

    HorizontalSpacing = 2

    def __init__(self, qta_id, text="", final_stretch=True, icon_size=16, objectName=None):
        super().__init__(objectName=objectName)

        self.app = QtWidgets.QApplication.instance()

        self.icon_size = QtCore.QSize(icon_size, icon_size)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.icon = ThemedIcon(qta_id, size=icon_size)
        self.text = QtWidgets.QLabel(text)

        layout.addWidget(self.icon)
        layout.addSpacing(self.HorizontalSpacing)
        layout.addWidget(self.text)

        if final_stretch:
            layout.addStretch()

    def setText(self, text):
        self.text.setText(text)


class ThemedIcon(qta.IconWidget):
    def __init__(self, icon_id, size=16, color=None):
        if color is None:
            color = QtWidgets.QApplication.instance().theme.icon_color
        super().__init__(icon_id, color=color, size=size)
        self.icon_id = icon_id
        self.size = size

        app = QtWidgets.QApplication.instance()
        app.theme_changed.connect(self.theme_changed)

    def theme_changed(self, theme):
        self.setIcon(qta.icon(self.icon_id, color=theme.icon_color))


class ThemedQPushButton(QtWidgets.QPushButton):
    def __init__(self, *args, icon_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_id = icon_id
        self.app = QtWidgets.QApplication.instance()
        self.app.theme_changed.connect(self.theme_changed)
        self.theme_changed(self.app.theme)

    def theme_changed(self, theme):
        self.setIcon(qta.icon(self.icon_id, color=theme.icon_color))


class ThemedAction(QtGui.QAction):
    def __init__(self, *args, icon_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_id = icon_id
        self.app = QtWidgets.QApplication.instance()
        self.app.theme_changed.connect(self.theme_changed)
        self.theme_changed(self.app.theme)

    def theme_changed(self, theme):
        self.setIcon(qta.icon(self.icon_id, color=theme.icon_color))
