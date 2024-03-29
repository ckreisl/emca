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

from renderer.shape import Shape
import vtk
import logging


class Line(Shape):

    def __init__(self, start_pos, end_pos):
        self._start_pos = start_pos
        self._end_pos = end_pos

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

        super().__init__(poly_data)

    @property
    def start_pos(self):
        return self._start_pos

    @property
    def end_pos(self):
        return self._end_pos

    @property
    def size(self):
        return self.GetProperty().GetLineWidth()

    @size.setter
    def size(self, size):
        self.GetProperty().SetLineWidth(size)

    def reset_size(self):
        self.GetProperty().SetLineWidth(self._default_size)

    def reset_all(self):
        self.reset_size()
        self.reset_color()
        self.reset_color_diffuse()
        self.reset_color_specular()
