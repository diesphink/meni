import os
import shutil
import jsonpickle
import time
from utils import calculate_sha1
from worker import Worker
from PySide6 import QtWidgets, QtCore, QtGui
from mpl_toolkits import mplot3d
import vtkplotlib as vpl
from stl.mesh import Mesh
from matplotlib import pyplot


class Local3DFile:
    def __init__(self, path, title=None, tags=None, hash=None, tags_path=None):
        self.path = path
        self.tags = tags or []
        self.process()

    def process(self):
        app = QtCore.QCoreApplication.instance()
        app.status.emit("Processing " + self.path)

        self.title = os.path.basename(self.path)
        self.hash = calculate_sha1(self.path)
        self.tags_path = sorted([app.metadata.tag_by_name(tag) for tag in self.tags], key=lambda x: x.quantity, reverse=True)
        self.generate_thumbnail()
        app.status.emit("Processing " + self.path + " done")
        app.metadata.changed.emit()

    def generate_thumbnail(self):

        app = QtCore.QCoreApplication.instance()

        # Read the STL using numpy-stl
        mesh = Mesh.from_file(self.path)

        import numpy as np

        # Plot the mesh
        vpl.figure()

        fig = vpl.figure()
        fig.background_color = "#282828"
        vpl.mesh_plot(mesh, color="#8ec07c")
        vpl.view(focal_point=[0, 0, 0], camera_position=[-50, -50, 50])
        vpl.reset_camera()
        # fig.show()

        # Show the figure
        vpl.save_fig(os.path.join(app.current_library, "thumbnails", f"{self.hash}.png"), off_screen=True)

    def from_dict(data):
        return Local3DFile(data["path"], data["title"], data["tags"], data["hash"], data["tags_path"])

    def to_dict(self):
        return {"path": self.path, "title": self.title, "tags": self.tags, "hash": self.hash, "tags_path": self.tags_path}

    def __str__(self):
        return f"{self.title} ({self.path})"

    def __repr__(self):
        return f"Local3DFile: {self.path}"


class Tag:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def from_dict(data):
        return Tag(data["name"], data["quantity"])

    def to_dict(self):
        return {"name": self.name, "quantity": self.quantity}

    def __str__(self):
        return f"{self.name} ({self.quantity})"

    def __repr__(self):
        return f"Tag: {self.name}"


class Metadata(QtCore.QObject):
    changed = QtCore.Signal()

    def __init__(self, files):
        super().__init__()
        self._load()
        self.changed.connect(self._save)
        self.app = QtCore.QCoreApplication.instance()

    @property
    def tags(self):
        self._tags = {}
        for file in self.files:
            for tag in file.tags:
                if tag not in self._tags:
                    self._tags[tag] = Tag(tag, 1)
                else:
                    self._tags[tag].quantity += 1
        return list(self._tags.values())

    def tag_by_name(self, name):
        return self._tags[name]

    def import_local_file(self, path):
        self.app.threadpool.start(Worker(self._background_import, path))

    def _background_import(self, path):
        self.app.status.emit("Importing " + path)

        new_path = shutil.copy(path, self.app.current_library)
        new_file = Local3DFile(new_path)
        self.files.append(new_file)
        self.changed.emit()
        self.app.status.emit("Importing " + path + " done")

    def _save(self):
        with open(os.path.join(".", "metadata.json"), "w") as outfile:
            outfile.write(jsonpickle.encode(self.files))

    def _load(self):
        if os.path.exists(os.path.join(".", "metadata.json")):
            with open(os.path.join(".", "metadata.json"), "r") as infile:
                self.files = jsonpickle.decode(infile.read())

    def reprocess_files(self):
        for file in self.files:
            file.process()

    def update_file(self, file, title=None, tags=None):
        print(tags)
        if title:
            file.title = title
        if tags:
            file.tags = tags
        self.changed.emit()
