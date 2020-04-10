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

import vtk
import random
import logging


class Ray(vtk.vtkActor):

    """
        Ray
        Visualizes one path segment within the 3D viewer (vtkRenderer)
        Can be incoming, outgoing, next event estimation or a path which ends in the environment map.
        Paths are colored differently, default white, envmap yellow, nee blue, red, depending if it is occluded or not,
        green if the segment is selected (always the incoming ray)
    """

    def __init__(self, start_pos, end_pos, is_ne=False, is_ne_occluded=False, is_envmap=False):
        vtk.vtkActor.__init__(self)

        self._start_pos = start_pos
        self._end_pos = end_pos
        self._is_ne = is_ne
        self._is_envmap = is_envmap

        pts = vtk.vtkPoints()
        pts.InsertNextPoint(start_pos.x, start_pos.y, start_pos.z)
        pts.InsertNextPoint(end_pos.x, end_pos.y, end_pos.z)
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, 0)
        line.GetPointIds().SetId(1, 1)
        segment = vtk.vtkCellArray()
        segment.InsertNextCell(line)
        poly_data = vtk.vtkPolyData()
        poly_data.SetPoints(pts)
        poly_data.SetLines(segment)
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(poly_data)
        else:
            mapper.SetInputData(poly_data)
        self.SetMapper(mapper)

        # normal color of ray is white
        self._color = [1, 1, 1]
        # color if selected
        self._selected_color = [0, 1, 0]
        if is_ne:
            # mark rays which are next event estimations
            if is_ne_occluded:
                # mark occluded as red
                self._color = [1, 0, 0]
            else:
                # mark not occluded as blue
                self._color = [0, 0, 1]
        elif is_envmap:
            # mark rays which hit the envmap
            self._color = [1, 1, 0]

        self.GetProperty().SetColor(self._color)

    @property
    def color(self):
        """
        Returns the color of the ray
        :return: vtkColor
        """
        return self.GetProperty().GetColor()

    def set_color_list(self, color):
        """
        Sets the color of the ray
        :param color: list[r,g,b]
        :return:
        """
        self.GetProperty().SetColor(color)

    def set_color_rgb(self, r, g, b):
        """
        Sets the color of the ray
        :param r: red
        :param g: green
        :param b: blue
        :return:
        """
        self.GetProperty().SetColor([r, g, b])

    @property
    def is_ne(self):
        """
        Returns if the path is a next event estimation segment
        :return: boolean
        """
        return self._is_ne

    @property
    def is_envmap(self):
        """
        Returns if the path is a ray which ends in an environment map
        :return: boolean
        """
        return self._is_envmap

    @property
    def start_pos(self):
        """
        Returns the start position of the ray
        :return: point3f
        """
        return self._start_pos

    @property
    def end_pos(self):
        """
        Returns the end position of the ray
        :return: point3f
        """
        return self._end_pos

    @property
    def opacity(self):
        """
        Returns the opacity of the ray
        :return: float[0,1]
        """
        return self.GetProperty().GetOpacity()

    @property
    def thickness(self):
        """
        Returns the thickness of the ray
        :return: float[0,1]
        """
        return self.GetProperty().GetLineWidth()

    @property
    def default_opacity(self):
        """
        Returns the default opacity 1.0
        :return: float
        """
        return 1.0

    @property
    def default_size(self):
        """
        Returns the default size 1.0
        :return: float
        """
        return 1.0

    def set_size(self, value):
        """
        Sets the size of the ray
        :param value: float[0,1]
        :return:
        """
        self.GetProperty().SetLineWidth(value)

    def set_opacity(self, value):
        """
        Sets the opacity of the ray
        :param value: float[0,1]
        :return:
        """
        self.GetProperty().SetOpacity(value)

    def set_selected(self, selected):
        """
        Highlight the ray, depending on input selected
        :param selected: boolean
        :return:
        """
        if selected:
            self.GetProperty().SetColor(self._selected_color)
        else:
            self.GetProperty().SetColor(self._color)

    def reset(self):
        """
        Resets the ray, opacity, thickness and color
        :return:
        """
        self.GetProperty().SetOpacity(self.default_opacity)
        self.GetProperty().SetLineWidth(self.default_size)
        self.GetProperty().SetColor(self._color)
