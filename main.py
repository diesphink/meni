from PySide6 import QtWidgets, QtCore
from qt_material import apply_stylesheet
from ui.windows.mainwindow import MainWindow
from ui.windows.welcome import WelcomeWindow
from app import App3dLibrary
import sys
import qdarkstyle


if __name__ == "__main__":
    app = App3dLibrary(sys.argv)

    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())

    # setup stylesheet
    # apply_stylesheet(app, theme="dark_teal.xml")
    # extra = {"density_scale": "-3"}
    # apply_stylesheet(app, "dark_teal.xml", invert_secondary=False, extra=extra, save_as="stylesheet.css")

    app.startup()

    app.exec()
