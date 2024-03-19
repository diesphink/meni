from PySide6 import QtWidgets, QtCore, QtGui


class LabelTree(QtWidgets.QWidget):
    """
    Class to show content of the tags in metadata in a tree view
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tags")
        self.setMaximumWidth(200)

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setAlternatingRowColors(True)
        self.tree.doubleClicked.connect(self.on_tree_double_clicked)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.tree)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.populate_tree()
        app = QtCore.QCoreApplication.instance()
        app.metadata.changed.connect(self.populate_tree)

    def populate_tree(self):

        app = QtCore.QCoreApplication.instance()

        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(["Tags"])
        self.tree.header().setVisible(False)
        self.tree.clear()

        for tag in sorted(app.metadata.tags, key=lambda x: x.quantity, reverse=True):
            item = QtWidgets.QTreeWidgetItem(self.tree, [str(tag)])
            item.tag = tag
            self.tree.addTopLevelItem(item)
            self.tree.expandItem(item)

    def on_tree_double_clicked(self, index):
        app = QtCore.QCoreApplication.instance()

        item = self.tree.currentItem()
        tag = item.tag
        font = QtGui.QFont()

        app.toggle_tag_filter(tag)
        font.setBold(app.is_tag_filtered(tag))
        item.setFont(0, font)
        self.repaint()
