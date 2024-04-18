import os
import shutil
import jsonpickle
from meni.utils import calculate_sha1
from PySide6 import QtCore
import vtkplotlib as vpl
from stl.mesh import Mesh


class Metadata(QtCore.QObject):
    changed = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.app = QtCore.QCoreApplication.instance()

        self.collections = []
        self.files = []
        self._tags = None
        self._authors = None

        self.changed.connect(self.clear_caches)
        self.changed.connect(self.validate)

    def clear_caches(self):
        self._tags = None
        self._authors = None

    def reload(self):
        self.clear_caches()
        self.changed.emit()

    def validate(self):
        # Collections without any file and with no data
        for collection in self.collections:
            if (
                collection.files == []
                and collection.attachments == []
                and collection.notes is None
                and collection.author is None
                and collection.url is None
            ):
                self.remove_collection(collection)

    @property
    def tags(self):
        if not self._tags:
            self._tags = {}
            for file in self.files:
                for tag in file.tags:
                    if tag not in self._tags:
                        self._tags[tag] = Tag(tag, 1)
                    else:
                        self._tags[tag].quantity += 1

        return list(self._tags.values())

    @property
    def authors(self):
        if not self._authors:
            self._authors = {}
            for collection in self.collections:
                author = collection.author
                if author is None:
                    author = "<No author>"
                if author not in self._authors:
                    self._authors[author] = len(collection.files)
                else:
                    self._authors[author] += len(collection.files)
        return list(self._authors.keys())

    def add_file(self, path, collection=None, name=None, tags=[]):
        new_path = shutil.copy(path, self.app.current_library)

        if name is None:
            name = os.path.basename(new_path)

        self.add_collection_if_not_exist(collection)

        hash = calculate_sha1(new_path)

        file = Local3DFile(new_path, collection, name, tags, hash)
        file.generate_thumbnail()
        self.files.append(file)
        self.changed.emit()

        return file

    def update_file(self, file, name=None, tags=None, collection=None, path=None):
        if name is not None:
            file.name = name
        if tags is not None:
            file.tags = tags
        if collection is not None:
            self.add_collection_if_not_exist(collection)
            file.collection = collection
        if path is not None:
            file.path = path

        self.changed.emit()
        return file

    def remove_file(self, file):
        try:
            os.remove(file.path)
        except FileNotFoundError:
            print(f"File not found: {file.path}")
            pass
        self.files.remove(file)
        self.changed.emit()

    def replace_file(self, file, path):
        os.remove(file.path)
        new_path = shutil.copy(path, self.app.current_library)
        file.path = new_path
        file.hash = calculate_sha1(new_path)
        file.generate_thumbnail()
        self.changed.emit()

        return file

    def add_collection(self, name, author=None, url=None, notes=None, attachments=[]):
        collection = Collection(name, author, url, notes, attachments)
        self.collections.append(collection)
        self.changed.emit()
        return collection

    def add_collection_if_not_exist(self, name, author=None, url=None, notes=None, attachments=[]):
        if self.collection_by_name(name) is None and name is not None and name.strip() != "":
            return self.add_collection(name, author, url, notes, attachments)

    def update_collection(self, collection, name=None, author=None, url=None, notes=None):
        if name is not None:
            for file in collection.files:
                file.collection = name
            collection.name = name
        if author is not None:
            collection.author = author
        if url is not None:
            collection.url = url
        if notes is not None:
            collection.notes = notes
        self.changed.emit()
        return collection

    def remove_collection(self, collection):
        for file in collection.files:
            self.remove_file(file)
        self.collections.remove(collection)
        self.changed.emit()

    def add_attachment(self, collection, path):
        new_path = shutil.copy(path, os.path.join(collection.attachments_folder, os.path.basename(path)))
        collection.attachments.append(new_path)
        self.changed.emit()
        return new_path

    def rename_attachment(self, collection, attachment, new_name):
        new_path = os.path.join(collection.attachments_folder, new_name)
        os.rename(attachment, new_path)
        collection.attachments.remove(attachment)
        collection.attachments.append(new_path)
        self.changed.emit()
        return new_path

    def remove_attachment(self, collection, attachment):
        os.remove(attachment)
        collection.attachments.remove(attachment)
        self.changed.emit()

    def commit_stage(self, stage):
        for file in stage.files:
            self.add_file(path=file.path, name=file.name, collection=stage.collection, tags=stage.tags)

    # GETTERS

    # def tag_by_name(self, name):
    #     return self._tags[name]

    # def file_by_hash(self, hash):
    #     for file in self.files:
    #         if file.hash == hash:
    #             return file

    # def file_by_name(self, name):
    #     for file in self.files:
    #         if file.name == name:
    #             return file

    # def file_by_path(self, path):
    #     for file in self.files:
    #         if file.path == path:
    #             return file

    # def file_by_library_path(self, library_path):
    #     for file in self.files:
    #         if file.library_path == library_path:
    #             return file

    def collection_by_name(self, name):
        for collection in self.collections:
            if collection.name == name:
                return collection


class JsonPickledMetadata(Metadata):
    def __init__(self):
        super().__init__()
        if QtCore.QCoreApplication.instance().current_library:
            os.makedirs(QtCore.QCoreApplication.instance().current_library, exist_ok=True)
            os.makedirs(os.path.join(QtCore.QCoreApplication.instance().current_library, "attachments"), exist_ok=True)
            os.makedirs(os.path.join(QtCore.QCoreApplication.instance().current_library, "thumbnails"), exist_ok=True)

            self.json_file = os.path.join(QtCore.QCoreApplication.instance().current_library, "metadata.json")

            self._load()
        self.changed.connect(self._save)

    def reload(self):
        self.json_file = os.path.join(QtCore.QCoreApplication.instance().current_library, "metadata.json")
        self._load()
        super().reload()

    def _save(self):
        with open(self.json_file, "w") as outfile:
            outfile.write(jsonpickle.encode({"collections": self.collections, "files": self.files}))

    def _load(self):
        self.files.clear()
        self.collections.clear()

        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as infile:
                obj = jsonpickle.decode(infile.read())
                self.files.extend(obj["files"])
                self.collections.extend(obj["collections"])


class Collection:
    def __init__(self, name, notes=None, author=None, url=None, attachments=[]):
        self.name = name
        self.notes = notes
        self.author = author
        self.url = url
        self.attachments = attachments

    @property
    def files(self):
        app = QtCore.QCoreApplication.instance()
        return [file for file in app.metadata.files if file.collection_obj == self]

    @property
    def attachments_folder(self):
        return os.path.join(QtCore.QCoreApplication.instance().current_library, "attachments", self.name)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Collection: {self.name}"


class Local3DFile:
    def __init__(self, path, collection, name=None, tags=None, hash=None):
        self.name = name or Local3DFile._name_from_path(path)
        self.path = path
        self.collection = collection
        self.tags = tags or []
        self.hash = hash or calculate_sha1(path)

    def _name_from_path(path):
        name = os.path.basename(path)
        name = os.path.splitext(name)[0]
        name = name.replace("_", " ")
        name = name.replace("-", " ")
        name = " ".join([word.capitalize() for word in name.split()])
        return name

    @property
    def absolute_path(self):
        return os.path.abspath(self.path)

    @property
    def thumbnail_file(self):
        return os.path.join(QtCore.QCoreApplication.instance().current_library, "thumbnails", f"{self.hash}.png")

    @property
    def collection_obj(self):
        metadata = QtCore.QCoreApplication.instance().metadata
        collection = metadata.collection_by_name(self.collection)
        if collection is None and self.collection is not None and self.collection.strip() != "":
            collection = metadata.add_collection(self.collection)
        return collection

    def generate_thumbnail(self):
        mesh = Mesh.from_file(self.path)
        fig = vpl.figure()
        fig.background_opacity = 0
        vpl.mesh_plot(mesh, color="#8ec07c", fig=fig)
        # vpl.view(focal_point=[0, 0, 0], camera_position=[-50, -50, 50], fig=fig)
        vpl.reset_camera(fig=fig)
        vpl.save_fig(self.thumbnail_file, off_screen=True, fig=fig)
        vpl.close(fig=fig)

    def __str__(self):
        return f"{self.name} ({self.path})"

    def __repr__(self):
        return f"Local3DFile: {self.path}"


class Tag:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} ({self.quantity})"

    def __repr__(self):
        return f"Tag: {self.name}"


class Stage:
    def __init__(self):
        self.files = []
        self.collection = None
        self.tags = []

    def __str__(self):
        return f"{self.collection} ({len(self.files)} files)"

    def __repr__(self):
        return f"Stage: {self.collection}"
