from PySide6 import QtWidgets, QtCore, QtGui
from meni.ui.common import DockTitleBar
from enum import IntFlag, auto
import qtawesome as qta


class DeselectableTreeView(QtWidgets.QTreeView):
    def mousePressEvent(self, event):

        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            index = self.indexAt(event.pos())
            if not index.isValid():
                self.clearSelection()

        super().mousePressEvent(event)


class BrowserDock(QtWidgets.QDockWidget):
    def __init__(self, parent):
        super().__init__("Browser", objectName="browser", parent=parent)
        self.setStyleSheet("background: transparent;")

        self.app = QtCore.QCoreApplication.instance()
        self.app.add_filter(self.filter)

        self.setTitleBarWidget(DockTitleBar("Browser", clicked=self.close))

        self.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.setAllowedAreas(QtCore.Qt.DockWidgetArea.AllDockWidgetAreas)

        self.tree = DeselectableTreeView()
        self.tree.setIndentation(10)
        self.tree.setRootIsDecorated(True)
        self.tree.setHeaderHidden(True)
        self.model = BrowserModel()
        self.tree.setModel(self.model)
        self.tree.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.tree.header().setStretchLastSection(False)
        self.tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tree.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.setWidget(self.tree)

        self.tree.setStyleSheet(
            f"""
                QTreeView::item {{
                    padding: 3px 0px;
                }}
            """
        )

        self.app.metadata.changed.connect(self.model.refresh)
        self.tree.clicked.connect(self.on_click)

    def on_click(self, index):
        item = self.model.get_item(index)
        if TreeItemType.ROOT_FOLDER not in item.type:
            if self.model.highlighted == item:
                self.model.highlighted = None
            else:
                self.model.highlighted = item
            self.app.filter_changed.emit()
        else:
            if self.tree.isExpanded(index):
                self.tree.collapse(index)
            else:
                self.tree.expand(index)

    def filter(self, file):
        highlighted = self.model.highlighted
        if highlighted:
            if TreeItemType.TAG in highlighted.type:
                if TreeItemType.NO_VALUE in highlighted.type:
                    return len(file.tags) == 0
                for tag in file.tags:
                    if tag.startswith(highlighted.data):
                        return True
            if TreeItemType.COLLECTION in highlighted.type:
                if TreeItemType.NO_VALUE in highlighted.type:
                    return file.collection is None or file.collection.strip() == ""
                return file.collection and file.collection.startswith(highlighted.data)
            if TreeItemType.AUTHOR in highlighted.type:
                if TreeItemType.NO_VALUE in highlighted.type:
                    return file.collection_obj is None or not file.collection_obj.author
                return file.collection_obj and file.collection_obj.author == highlighted.data
            return False

        return True


class BrowserModel(QtCore.QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self.app = QtCore.QCoreApplication.instance()
        self._highlighted = None
        self.root_item = BrowserTreeItem("root", None, TreeItemType.ROOT_FOLDER)

        self.tags_item = self.root_item.append_child("Tags", TreeItemType.ROOT_FOLDER | TreeItemType.TAG)
        self.collections_item = self.root_item.append_child("Collections", TreeItemType.ROOT_FOLDER | TreeItemType.COLLECTION)
        self.authors_item = self.root_item.append_child("Authors", TreeItemType.ROOT_FOLDER | TreeItemType.AUTHOR)

        self.notags_item = self.tags_item.append_child("No Tags", TreeItemType.NO_VALUE | TreeItemType.TAG)
        self.nocollections_item = self.collections_item.append_child("No Collection", TreeItemType.NO_VALUE | TreeItemType.COLLECTION)
        self.noauthor_item = self.authors_item.append_child("No Author", TreeItemType.NO_VALUE | TreeItemType.AUTHOR)

        self.refresh()

    def data(self, index: QtCore.QModelIndex, role: int):
        if not index.isValid():
            return None

        item: BrowserTreeItem = self.get_item(index)

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                text = item.text
                if item == self.highlighted:
                    text = f"{text} (filtered)"
                if TreeItemType.ROOT_FOLDER in item.type:
                    text = f"[ {text.upper()} ]"
                return text
            elif index.column() == 1:
                if TreeItemType.ROOT_FOLDER not in item.type:
                    return item.count

        elif role == QtCore.Qt.ItemDataRole.DecorationRole and index.column() == 0:

            if item == self.highlighted:
                icon = "fa5s.filter"
            elif TreeItemType.ROOT_FOLDER | TreeItemType.TAG in item.type:
                icon = "fa5s.tags"
            elif TreeItemType.ROOT_FOLDER | TreeItemType.COLLECTION in item.type:
                icon = "fa5s.layer-group"
            elif TreeItemType.ROOT_FOLDER | TreeItemType.AUTHOR in item.type:
                icon = "fa5s.user-friends"
            elif TreeItemType.NO_VALUE in item.type:
                icon = "fa5s.minus-circle"
            elif TreeItemType.TAG in item.type:
                icon = "fa5s.tag"
            elif TreeItemType.COLLECTION in item.type:
                icon = "fa5s.th-large"
            elif TreeItemType.AUTHOR in item.type:
                icon = "fa5s.user"

            color = self.app.theme.icon_color
            if self.highlighted:
                if self.highlighted != item and not self.highlighted.path.startswith(item.path):
                    color = self.app.theme.muted

            return qta.icon(icon, color=color)

        elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole and index.column() == 1:
            return QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter

        elif role == QtCore.Qt.ItemDataRole.FontRole and (
            item == self.highlighted or (self.highlighted and self.highlighted.path.startswith(item.path))
        ):
            font = self.app.font()
            font.setBold(True)
            return font

        elif role == QtCore.Qt.ItemDataRole.ForegroundRole:
            if self.highlighted:
                if self.highlighted != item and not self.highlighted.path.startswith(item.path):
                    return QtGui.QColor(self.app.theme.muted)
            if TreeItemType.ROOT_FOLDER in item.type:
                return QtGui.QColor(self.app.theme.icon_color)

        return None

    def index(self, row: int, column: int, parent: QtCore.QModelIndex = QtCore.QModelIndex()):
        parent_item: BrowserTreeItem = self.get_item(parent)

        if not parent_item:
            return QtCore.QModelIndex()

        child_item: BrowserTreeItem = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex):
        if not index.isValid():
            return QtCore.QModelIndex()

        child_item: BrowserTreeItem = self.get_item(index)
        if child_item:
            parent_item: BrowserTreeItem = child_item.parent()
        else:
            parent_item = None

        if parent_item == self.root_item or not parent_item:
            return QtCore.QModelIndex()
        return self.createIndex(parent_item.child_number(), 0, parent_item)

    def columnCount(self, parent: QtCore.QModelIndex):
        return 2

    def rowCount(self, parent: QtCore.QModelIndex):
        parent_item: BrowserTreeItem = self.get_item(parent)
        if parent_item:
            return len(parent_item.children)
        return 0

    def get_item(self, index: QtCore.QModelIndex):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.root_item

    def get_item_by_path(self, path):
        return self.root_item.child_by_path(path)

    def refresh(self):
        metadata = QtCore.QCoreApplication.instance().metadata

        self.layoutAboutToBeChanged.emit()
        self.root_item.reset()

        for file in metadata.files:

            tags = file.tags
            if len(tags) == 0:
                self.notags_item.count += 1
            else:
                for tag in tags:
                    tag_path = ["Tags"]
                    for tag_part in tag.split("/"):
                        tag_path = tag_path + [tag_part]
                        tag_item = self.get_item_by_path(tag_path)
                        if tag_item is None:
                            tag_item = self.get_item_by_path(tag_path[:-1]).append_child("/".join(tag_path[1:]), TreeItemType.TAG)
                            tag_item.count = 0
                        tag_item.count += 1

            coll = file.collection
            if coll is None or coll.strip() == "":
                self.nocollections_item.count += 1
            else:
                coll_path = ["Collections"]
                for coll_part in coll.split("/"):
                    coll_path = coll_path + [coll_part]
                    coll_item = self.get_item_by_path(coll_path)
                    if coll_item is None:
                        coll_item = self.get_item_by_path(coll_path[:-1]).append_child("/".join(coll_path[1:]), TreeItemType.COLLECTION)
                        coll_item.count = 0
                    coll_item.count += 1

            author = file.collection_obj.author if file.collection_obj and file.collection_obj.author else None
            if author is None or author.strip() == "":
                self.noauthor_item.count += 1
            else:
                author_item = self.get_item_by_path(["Authors", author])
                if author_item is None:
                    author_item = self.get_item_by_path(["Authors"]).append_child(author, TreeItemType.AUTHOR)
                    author_item.count = 0
                author_item.count += 1

        self.layoutChanged.emit()

    @property
    def highlighted(self):
        return self._highlighted

    @highlighted.setter
    def highlighted(self, item):
        self.layoutAboutToBeChanged.emit()
        self._highlighted = item
        self.layoutChanged.emit()

    def flags(self, index: QtCore.QModelIndex | QtCore.QPersistentModelIndex) -> QtCore.Qt.ItemFlag:
        return QtCore.Qt.ItemFlag.ItemIsEnabled


class TreeItemType(IntFlag):
    ROOT_FOLDER = auto()
    TAG = auto()
    COLLECTION = auto()
    AUTHOR = auto()
    NO_VALUE = auto()


class BrowserTreeItem:
    def __init__(self, data, parent: "BrowserTreeItem", type: TreeItemType):
        self.data = data
        self.parent_item = parent
        self.children = []
        self.count = 0
        self.type = type

    def child(self, row: int) -> "BrowserTreeItem":
        if row >= len(self.children) or row < 0:
            return None
        return self.children[row]

    def child_by_path(self, path):
        for item in self.children:
            if item.text == path[0]:
                if len(path) == 1:
                    return item
                return item.child_by_path(path[1:])
        return None

    @property
    def text(self):
        return self.data.split("/")[-1]

    def child_number(self) -> int:
        if self.parent_item:
            return self.parent_item.children.index(self)
        return 0

    def append_child(self, data, type: TreeItemType) -> "BrowserTreeItem":
        child = BrowserTreeItem(data, self, type)
        self.children.append(child)
        return child

    @property
    def path(self):
        if self.parent():
            return f"{self.parent().path}/{self.text}"
        else:
            return self.text

    def reset(self):
        self.count = 0
        for child in self.children:
            child.reset()

    def parent(self) -> "BrowserTreeItem":
        return self.parent_item

    def __repr__(self):
        return f"BrowserTreeItem({self.type}, {self.path})"
