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

from renderer.line import Line
from core.color3 import Color3f
import vtk


class Ray(Line):

    """
        Ray
        Visualizes one path segment within the 3D viewer (vtkRenderer)
        Can be incoming, outgoing, next event estimation or a path which ends in the environment map.
        Paths are colored differently, default white, envmap yellow, nee blue, red, depending if it is occluded or not,
        green if the segment is selected (always the incoming ray)
    """

    def __init__(self, start_pos, end_pos, is_ne=False, is_ne_occluded=False, is_envmap=False):

        self._is_ne = is_ne
        self._is_ne_occluded = is_ne_occluded
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

        # normal color of ray is white
        color = Color3f(1, 1, 1)
        # color if selected
        selected_color = Color3f(0, 1, 0)
        if is_ne:
            # mark rays which are next event estimations
            if is_ne_occluded:
                # mark occluded as red
                color = Color3f(1, 0, 0)
            else:
                # mark not occluded as blue
                color = Color3f(0, 0, 1)
        elif is_envmap:
            # mark rays which hit the envmap
            color = Color3f(1, 1, 0)

        super().__init__(start_pos, end_pos)
        self.selected_color = selected_color
        self.color = color

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
    def is_ne_occluded(self):
        """
        Returns if the next event estimation is occluded
        :return: boolean
        """
        return self._is_ne_occluded

