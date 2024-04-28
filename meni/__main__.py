from PySide6 import QtWidgets, QtCore
from qt_material import apply_stylesheet
from meni.ui.windows.mainwindow import MainWindow
from meni.ui.windows.welcome import WelcomeWindow
from meni.app import AppMeni
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Meni: Library manager for 3D models and assets.")
    parser.add_argument("-l", "--library", help="Path to the library directory.")
    args = parser.parse_args()

    app = AppMeni(sys.argv, library=args.library)

    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())

    # setup stylesheet
    # apply_stylesheet(app, theme="dark_teal.xml")
    # extra = {"density_scale": "-3"}
    # apply_stylesheet(app, "dark_teal.xml", invert_secondary=False, extra=extra, save_as="stylesheet.css")

    app.startup()

    app.exec()


if __name__ == "__main__":
    main()
