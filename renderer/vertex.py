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


class Vertex(Shape):

    def __init__(self, pos):
        self._pos = pos
        pts = vtk.vtkPoints()
        pts.InsertNextPoint(pos.x, pos.y, pos.z)
        verts = vtk.vtkCellArray()
        vertex = vtk.vtkVertex()
        vertex.GetPointIds().SetId(0, 0)
        verts.InsertNextCell(vertex)
        poly_data = vtk.vtkPolyData()
        poly_data.SetPoints(pts)
        poly_data.SetVerts(verts)
        super().__init__(poly_data)

    @property
    def pos(self):
        """
        Returns the position of the vertex
        :return: Point3f
        """
        return self._pos
