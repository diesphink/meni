import importlib.metadata
from PySide6 import QtWidgets, QtCore
from qt_material import apply_stylesheet
from meni.ui.windows.mainwindow import MainWindow
from meni.ui.windows.welcome import WelcomeWindow
from meni.app import AppMeni
import sys
import argparse
import os
import importlib


def main():
    parser = argparse.ArgumentParser(description="Meni: Library manager for 3D models and assets.")
    parser.add_argument("-l", "--library", help="Path to the library directory.")
    parser.add_argument("-w", "--wayland", help="Support for wayland (set QT_QPA_PLATFORM=xcb)", action="store_true")
    parser.add_argument("-v", "--version", action="version", version=f"meni {importlib.metadata.version('meni')}")
    parser.add_argument("--welcome", help="Show welcome screen", action="store_true")
    args = parser.parse_args()

    if args.wayland:
        os.environ["QT_QPA_PLATFORM"] = "xcb"

    app = AppMeni(sys.argv, library=args.library)

    if args.welcome:
        app.show_welcome()
    else:
        app.startup()

    app.exec()


if __name__ == "__main__":
    main()
