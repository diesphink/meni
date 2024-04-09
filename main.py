from PySide6 import QtWidgets, QtCore
from qt_material import apply_stylesheet
from ui.windows.mainwindow import MainWindow
from ui.windows.welcome import WelcomeWindow
from app import App3dLibrary
import sys
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="3D Library: Library manager for 3D models and assets.")
    parser.add_argument("-l", "--library", help="Path to the library directory.")
    args = parser.parse_args()

    app = App3dLibrary(sys.argv, library=args.library)

    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())

    # setup stylesheet
    # apply_stylesheet(app, theme="dark_teal.xml")
    # extra = {"density_scale": "-3"}
    # apply_stylesheet(app, "dark_teal.xml", invert_secondary=False, extra=extra, save_as="stylesheet.css")

    app.startup()

    app.exec()
