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

from PySide2.QtWidgets import QListWidgetItem
import logging


class PathListItem(QListWidgetItem):

    def __init__(self, path_index):
        super().__init__()
        self._path_index = path_index
        self.setText("Path ({})".format(path_index))

    @property
    def path_index(self):
        return self._path_index


class IntersectionListItem(QListWidgetItem):

    def __init__(self, tpl):
        super().__init__()
        self._tpl = tpl
        self.setText("Intersection ({})".format(tpl[1]))

    @property
    def path_index(self):
        """
        Returns the index of the parent, representing the path index
        :return: integer
        """
        return self._tpl[0]

    @property
    def intersection_index(self):
        """
        Returns the intersection index
        :return: integer
        """
        return self._tpl[1]

    @property
    def index_tpl(self):
        """
        Returns a tuple containing path and intersection index
        :return: tuple(path_index, intersection_index)
        """
        return self._tpl
