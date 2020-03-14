"""
    This file is part of EMCA, an explorer of Monte-Carlo based Algorithms.
    Copyright (c) 2019-2020 by Christoph Kreisl and others.
    EMCA is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License Version 3
    as published by the Free Software Foundation.
    EMCA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import vtk
import logging


class Vertex(vtk.vtkActor):

    """
        Vertex
        Represents and visualizes one vertex within the 3D scene viewer
    """

    def __init__(self, path_idx, vertex_idx, pos):
        vtk.vtkActor.__init__(self)

        self._path_idx = path_idx
        self._vertex_idx = vertex_idx

        self._pos = pos
        pts = vtk.vtkPoints()
        pts.InsertNextPoint(pos.x, pos.y, pos.z)
        verts = vtk.vtkCellArray()
        vertex = vtk.vtkVertex()
        vertex.GetPointIds().SetId(0, 0)
        verts.InsertNextCell(vertex)
        polyData = vtk.vtkPolyData()
        polyData.SetPoints(pts)
        polyData.SetVerts(verts)
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(polyData)
        else:
            mapper.SetInputData(polyData)
        self.SetMapper(mapper)

        self._color_selected = [1, 0.6, 0]
        self._color = [1, 1, 1]

        self.GetProperty().SetColor(self._color)

    @property
    def pos(self):
        """
        Returns the position of the vertex
        :return: point3f
        """
        return self._pos

    @property
    def path_index(self):
        """
        Returns the corresponding path index
        :return:
        """
        return self._path_idx

    @property
    def index(self):
        """
        Returns the index of the vertex
        :return:
        """
        return self._vertex_idx

    @property
    def size(self):
        """
        Returns the size
        :return:
        """
        return self.GetProperty().GetPointSize()

    @property
    def color(self):
        """
        Returns the color
        :return:
        """
        return self.GetProperty().GetColor()

    @property
    def opacity(self):
        """
        Returns the opacity
        :return:
        """
        return self.GetProperty().GetOpacity()

    @property
    def default_opacity(self):
        """
        Returns the default opacity 1.0
        :return:
        """
        return 1.0

    @property
    def default_size(self):
        """
        Returns the default size 1.0
        :return:
        """
        return 1.0

    def get_index_tpl(self):
        """
        Returns the index tuple based on the path and vertex index
        :return: tuple(path_index, vertex_index)
        """
        return self._path_idx, self._vertex_idx

    def set_opacity(self, value):
        """
        Sets the opacity of the vertex
        :param value: float [0,1]
        :return:
        """
        self.GetProperty().SetOpacity(value)

    def set_size(self, value):
        """
        Sets the size of the vertex
        :param value: float [0,1]
        :return:
        """
        self.GetProperty().SetPointSize(value)

    def set_selected(self, selected):
        """
        Highlight the vertex if it is selected
        :param selected: boolean
        :return:
        """
        if selected:
            self.GetProperty().SetColor(self._color_selected)
        else:
            self.GetProperty().SetColor(self._color)

    def reset(self):
        """
        Resets opacity, vertex size and its color to the default values
        :return:
        """
        self.GetProperty().SetOpacity(self.default_opacity)
        self.GetProperty().SetPointSize(self.default_size)
        self.GetProperty().SetColor(self._color)
