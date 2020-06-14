"""
    MIT License

    Copyright (c) 2020 Christoph Kreisl

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

from PySide2.QtWidgets import QTreeWidgetItem


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
