from PyQt5.QtWidgets import QTreeWidgetItem


class PathNodeItem(QTreeWidgetItem):

    """
        PathNodeItem
        Represents a Path Node within the tree view of the View Render Data
        Holds the path index if this item is selected.
        Necessary to know which path item is selected by the user.
    """

    def __init__(self, index):
        QTreeWidgetItem.__init__(self)
        self._index = index

    @property
    def index(self):
        """
        Returns the node index representing the path index
        :return:
        """
        return self._index


class VertexNodeItem(QTreeWidgetItem):

    """
        VertexNodeItem
        Represents a VertexNode within the tree view of the View Render Data
        Holds information about the parent index and the vertex index.
        Necessary to know which vertex and path item is selected by the user.
    """

    def __init__(self, parent_index, vertex_index):
        QTreeWidgetItem.__init__(self)

        self._parent_index = parent_index
        self._vertex_index = vertex_index

    @property
    def parent_index(self):
        """
        Returns the index of the parent, representing the path index
        :return: integer
        """
        return self._parent_index

    @property
    def index(self):
        """
        Returns the vertex index
        :return: integer
        """
        return self._vertex_index

    def index_tpl(self):
        """
        Returns a tuple containing path and vertex index
        :return: tuple(path_index, vertex_index)
        """
        return self._parent_index, self._vertex_index
