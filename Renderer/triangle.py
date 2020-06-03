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

from Renderer.shape import Shape
import vtk
import logging


class Triangle(Shape):

    """
        Triangle
        Represents a vtk Triangle object within the 3D scene
    """

    def __init__(self, p1, p2, p3):

        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        # create points
        points = vtk.vtkPoints()
        points.InsertNextPoint(p1.x, p1.y, p1.z)
        points.InsertNextPoint(p2.x, p2.y, p2.z)
        points.InsertNextPoint(p3.x, p3.y, p3.z)

        triangle = vtk.vtkTriangle()
        triangle.GetPointIds().SetId(0, 0)
        triangle.GetPointIds().SetId(1, 1)
        triangle.GetPointIds().SetId(2, 2)

        triangles = vtk.vtkCellArray()
        triangles.InsertNextCell(triangle)

        # polydata object
        triangle_poly_data = vtk.vtkPolyData()
        triangle_poly_data.SetPoints(points)
        triangle_poly_data.SetPolys(triangles)

        super().__init__(triangle_poly_data)

