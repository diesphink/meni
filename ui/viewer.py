import vtkplotlib as vpl
import numpy as np
from stl.mesh import Mesh
from PySide6 import QtWidgets, QtCore
import vtk


class Viewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.app = QtCore.QCoreApplication.instance()

        self.app.selected_file_changed.connect(self.on_selected_file_changed)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.mesh = None

        self.fig = vpl.QtFigure2()
        self.fig.vl.setContentsMargins(0, 0, 0, 0)
        self.fig.background_color = self.app.theme.main_background
        self.layout.addWidget(self.fig)
        self.fig.show()

    def on_selected_file_changed(self, file):
        self.show_stl(file.path)

    def show_stl(self, stl):
        if self.mesh:
            self.fig.remove_plot(self.mesh)
        self.mesh = vpl.mesh_plot(Mesh.from_file(stl), color=self.app.theme.model_color, fig=self.fig)
        vpl.reset_camera(fig=self.fig)
        self.fig.update()
