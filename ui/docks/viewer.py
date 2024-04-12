from PySide6 import QtWidgets, QtCore
from ui.tagrow import TagRow
from ui.common import DockTitleBar
from stl.mesh import Mesh
import vtkplotlib as vpl
import qtawesome as qta


class ViewerDock(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super().__init__("Viewer", objectName="viewer", parent=parent)

        self.app = QtCore.QCoreApplication.instance()
        self.mesh = None

        self.setTitleBarWidget(DockTitleBar("Viewer", clicked=self.close))

        self.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.setAllowedAreas(QtCore.Qt.DockWidgetArea.AllDockWidgetAreas)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(5, 5, 5, 5)

        # Title
        self.title = QtWidgets.QLabel()
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;text-decoration: underline;")
        self.title.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(self.title)

        # Path
        self.path = QtWidgets.QLabel()
        self.path.setStyleSheet("font-size: 10px; opacity: 0.8")
        self.layout.addWidget(self.path)

        # Tags
        self.tagrow = TagRow()
        self.tagrow.setContentsMargins(0, 10, 0, 0)
        self.layout.addWidget(self.tagrow)

        # Mesh viewer
        self.fig = vpl.QtFigure2()
        self.fig.vl.setContentsMargins(0, 0, 0, 0)
        self.fig.background_color = self.app.theme.main_background
        self.show_stl(None)
        self.layout.addWidget(self.fig)

        # Set layout to widget to dock
        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setWidget(widget)

        # Connect signals
        self.app.metadata.changed.connect(lambda: self.on_selected_file_changed(self.app.selected_file))
        self.app.selected_file_changed.connect(self.on_selected_file_changed)

    def on_selected_file_changed(self, file):
        if file:
            self.title.setText(file.name)
            self.path.setText(file.path)
            self.tagrow.tags = file.tags
            self.show_stl(file.path)
        else:
            self.title.setText("")
            self.path.setText("")
            self.tagrow.tags = []
            self.show_stl(None)

    def show_stl(self, stl):
        if self.mesh:
            self.fig.remove_plot(self.mesh)

        if stl is None:
            self.fig.update()
            return

        self.mesh = vpl.mesh_plot(Mesh.from_file(stl), color=self.app.theme.model_color, fig=self.fig)
        vpl.reset_camera(fig=self.fig)
        self.fig.update()
