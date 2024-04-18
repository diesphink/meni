import hashlib
from PySide6 import QtWidgets, QtGui

BUF_SIZE = 65536


def calculate_sha1(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


def calculate_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def horizontal_layout(*widgets, margins=[0, 0, 0, 0]):
    layout = QtWidgets.QHBoxLayout()
    layout.setContentsMargins(*margins)
    for widget in widgets:
        layout.addWidget(widget)
    return layout


def tags_from_text(text):
    return [tag.strip() for tag in text.split(",") if tag.strip()]


def pxmap_from_svg(svg_filepath, color="black"):
    img = QtGui.QPixmap(svg_filepath)
    qp = QtGui.QPainter(img)
    qp.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
    qp.fillRect(img.rect(), QtGui.QColor(color))
    qp.end()
    return img
