from PySide6 import QtWidgets, QtCore
import qtawesome as qta


class IconLabel(QtWidgets.QWidget):

    IconSize = QtCore.QSize(16, 16)
    HorizontalSpacing = 0

    def __init__(self, qta_id, text, final_stretch=True):
        super().__init__()

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        icon = QtWidgets.QLabel()
        icon.setPixmap(qta.icon(qta_id, color="#8ec07c").pixmap(self.IconSize))

        layout.addWidget(icon)
        layout.setSpacing(2)
        layout.addWidget(QtWidgets.QLabel(text))

        if final_stretch:
            layout.addStretch()
