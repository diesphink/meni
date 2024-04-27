from PySide6 import QtWidgets, QtCore
from meni.ui.tagrow import TagRow
from meni.ui.common import DockTitleBar, IconLabel
from stl.mesh import Mesh
import vtkplotlib as vpl
import qtawesome as qta


class ViewerDock(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super().__init__("Viewer", objectName="viewer", parent=parent)

        self.app = QtCore.QCoreApplication.instance()
        self.mesh_plot = None
        self.loader = None
        self.threadpool = QtCore.QThreadPool()

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

        self.layout.addSpacing(10)

        # Path
        self.path = IconLabel(qta_id="fa5s.file", icon_size=12)
        self.path.setStyleSheet("font-size: 10px; opacity: 0.8")
        self.layout.addWidget(self.path)

        # Collection
        self.collection = IconLabel(qta_id="fa5s.layer-group", icon_size=12, final_stretch=True)
        self.collection.setStyleSheet("font-size: 10px; opacity: 0.8")
        self.collection.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.layout.addWidget(self.collection)

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
        self.app.metadata.changed.connect(lambda: self.on_selected_file_changed([], self.app.last_selected_file))
        self.app.selected_files_changed.connect(self.on_selected_file_changed)

        # Starting values
        self.on_selected_file_changed([], None)

    def on_selected_file_changed(self, files, last):
        self.path.setVisible(last is not None)
        self.collection.setVisible(last is not None and last.collection_obj is not None)

        if last:
            self.title.setText(last.name)
            self.path.setText(last.path)
            self.collection.setText(last.collection_obj.name if last.collection_obj else "")
            self.tagrow.tags = last.tags
            self.show_stl(last.path)
        else:
            self.title.setText("")
            self.path.setText("")
            self.collection.setText("")
            self.tagrow.tags = []
            self.show_stl(None)

    def show_stl(self, stl):
        if stl is None:
            self.fig.update()
            return

        if self.loader:
            self.loader.cancel()

        self.loader = BackgroundLoader(stl)
        self.threadpool.start(self.loader)
        self.loader.signals.loaded.connect(self.on_mesh_loaded)

    def on_mesh_loaded(self, mesh):
        if self.mesh_plot:
            self.fig.remove_plot(self.mesh_plot)
        self.mesh_plot = vpl.mesh_plot(mesh, color=self.app.theme.model_color, fig=self.fig)
        vpl.reset_camera(fig=self.fig)
        self.fig.update()


class BackgroundLoader(QtCore.QRunnable):

    def __init__(self, path):
        super(BackgroundLoader, self).__init__()
        self.path = path
        self.cancelled = False
        self.signals = BackgroundLoaderSignals()

    @QtCore.Slot()
    def run(self):
        mesh = Mesh.from_file(self.path)
        if not self.cancelled:
            self.signals.loaded.emit(mesh)

    def cancel(self):
        self.cancelled = True


class BackgroundLoaderSignals(QtCore.QObject):
    loaded = QtCore.Signal(Mesh)
