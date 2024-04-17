from PySide6 import QtWidgets, QtCore
from ui.common import DockTitleBar
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

        self.setTitleBarWidget(DockTitleBar("Browser", clicked=self.close))

        self.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable | QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.setAllowedAreas(QtCore.Qt.DockWidgetArea.AllDockWidgetAreas)

        self.tree = DeselectableTreeView()
        self.tree.setIndentation(10)
        self.tree.setRootIsDecorated(True)
        self.tree.setHeaderHidden(True)
        self.model = BrowserModel()
        self.tree.setModel(self.model)

        self.tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tree.header().setStretchLastSection(False)

        self.setWidget(self.tree)

        self.tree.setStyleSheet(
            f"""
                QTreeView {{
                    border: none;
                    background: transparent;
                    show-decoration-selected: 0;
                }}
                QTreeView::item, QTreeView::item::hover, QTreeView::item::selected, QTreeView::item::!selected::focus, QTreeView::item::selected::active {{
                    padding: 5px;
                    margin: 0px;
                    border: none;
                    color: {self.app.theme.foreground};
                }}
                
                QTreeView::item:hover {{
                    background-color: rgba(255, 255, 255, 0.01);
                }}
                
                QTreeView::item:selected {{
                    background: {self.app.theme.selection_background} !important;
                    color: {self.app.theme.selection_foreground} !important;
                }}
                

                
                
                
            """
        )

        self.app.metadata.changed.connect(self.model.populate_cache)
        self.tree.doubleClicked.connect(self.on_double_click)

    def on_double_click(self, index):
        item = self.model.get_item(index)
        if self.model.highlighted == item:
            self.model.highlighted = None
        else:
            self.model.highlighted = item


class BrowserModel(QtCore.QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self.app = QtCore.QCoreApplication.instance()
        self._highlighted = None
        self.root_item = BrowserTreeItem("root")

        self.tags_item = self.root_item.append_child("Tags", "fa5s.tag")
        self.collections_item = self.root_item.append_child("Collections", "fa5s.layer-group")
        self.authors_item = self.root_item.append_child("Authors", "fa5s.user")

        self.populate_cache()

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

    def rowCount(self, parent: QtCore.QModelIndex):
        parent_item: BrowserTreeItem = self.get_item(parent)
        if not parent_item:
            return 0
        return parent_item.child_count()

    def columnCount(self, parent: QtCore.QModelIndex):
        return 2

    def data(self, index: QtCore.QModelIndex, role: int):
        if not index.isValid():
            return None

        item: BrowserTreeItem = self.get_item(index)
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            text = item.data(index.column())
            if index.column() == 0 and item == self.highlighted:
                return f"{text} (filtered)"
            return text

        elif role == QtCore.Qt.ItemDataRole.DecorationRole and index.column() == 0:
            if item == self.highlighted:
                return qta.icon("fa5s.filter", color=self.app.theme.icon_color)
            return qta.icon(item.icon, color=self.app.theme.icon_color)

        elif role == QtCore.Qt.ItemDataRole.TextAlignmentRole and index.column() == 1:
            return QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter

        elif role == QtCore.Qt.ItemDataRole.FontRole and (
            item == self.highlighted or (self.highlighted and self.highlighted.path.startswith(item.path))
        ):
            font = self.app.font()
            font.setBold(True)
            return font
        return None

    def get_item(self, index: QtCore.QModelIndex):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self.root_item

    def get_item_by_path(self, path):
        return self.root_item.child_by_path(path)

    def populate_cache(self):
        metadata = QtCore.QCoreApplication.instance().metadata

        self.layoutAboutToBeChanged.emit()
        for item in self.root_item.children:
            item.children = []

        for file in metadata.files:

            tags = file.tags
            if len(tags) == 0:
                tags = ["<No Tags>"]

            for tag in tags:
                tag_path = ["Tags"]
                for tag_part in tag.split("/"):
                    tag_path = tag_path + [tag_part]
                    tag_item = self.get_item_by_path(tag_path)
                    if tag_item is None:
                        tag_item = self.get_item_by_path(tag_path[:-1]).append_child(tag_part)
                        tag_item.count = 0
                    tag_item.count += 1

            coll = file.collection
            if coll is None or coll.strip() == "":
                coll = "<No Collection>"

            coll_path = ["Collections"]
            for coll_part in coll.split("/"):
                coll_path = coll_path + [coll_part]
                coll_item = self.get_item_by_path(coll_path)
                if coll_item is None:
                    coll_item = self.get_item_by_path(coll_path[:-1]).append_child(coll_part)
                    coll_item.count = 0
                coll_item.count += 1

            author = file.collection_obj.author if file.collection_obj and file.collection_obj.author else "<No Author>"
            author_item = self.get_item_by_path(["Authors", author])
            if author_item is None:
                author_item = self.get_item_by_path(["Authors"]).append_child(author)
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


class BrowserTreeItem:
    def __init__(self, text, parent: "BrowserTreeItem" = None, icon=None, count=None):
        self.text = text
        self.parent_item = parent
        self.children = []
        self.icon = icon or (parent.icon if parent else None)
        self.count = count

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

    def last_child(self) -> "BrowserTreeItem":
        return self.children[-1] if self.children else None

    def child_count(self) -> int:
        return len(self.children)

    def child_number(self) -> int:
        if self.parent_item:
            return self.parent_item.children.index(self)
        return 0

    def data(self, column: int) -> str:
        if column == 0:
            return self.text
        elif column == 1 and self.count is not None:
            return self.count

    def insert_child(self, position: int, text, icon=None) -> "BrowserTreeItem":
        if position < 0 or position > len(self.children):
            return False

        child = BrowserTreeItem(text, self, icon)
        self.children.insert(position, child)

        return child

    def append_child(self, text, icon=None) -> "BrowserTreeItem":
        return self.insert_child(len(self.children), text, icon)

    @property
    def path(self):
        if self.parent():
            return f"{self.parent().path}/{self.text}"
        else:
            return self.text

    def parent(self) -> "BrowserTreeItem":
        return self.parent_item

    def __repr__(self):
        return f"BrowserTreeItem({self.path})"
