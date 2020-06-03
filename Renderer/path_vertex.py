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

from Renderer.vertex import Vertex
from Types.color3 import Color3f
import logging


class PathVertex(Vertex):

    """
        Vertex
        Represents and visualizes one vertex within the 3D scene viewer
    """

    def __init__(self, path_idx, vertex_idx, pos):
        super(Vertex, self).__init__(pos)
        self.set_selected_color(Color3f(1, 0.6, 0))

        self._path_idx = path_idx
        self._vertex_idx = vertex_idx

    def get_path_index(self):
        """
        Returns the corresponding path index
        :return: integer
        """
        return self._path_idx

    def get_vertex_index(self):
        """
        Returns the index of the vertex
        :return: integer
        """
        return self._vertex_idx

    def get_index_tpl(self):
        """
        Returns the index tuple based on the path and vertex index
        :return: tuple(path_index, vertex_index)
        """
        return self._path_idx, self._vertex_idx
