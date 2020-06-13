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
import time


class Mesh(Shape):

    """
        Mesh
        Represents a Mesh object within the 3D scene as vtkActor
    """

    def __init__(self, mesh, opacity=0.25):

        start = time.time()

        vertices = vtk.vtkPoints()
        vertex_float_array = vtk.vtkFloatArray()
        vertex_float_array.SetArray(mesh.vertices, mesh.vertex_count*3, True)
        vertex_float_array.SetNumberOfComponents(3)
        vertex_float_array.SetNumberOfTuples(mesh.vertex_count)
        vertices.SetData(vertex_float_array)

        triangles = vtk.vtkCellArray()
        triangle_id_array = vtk.vtkIdTypeArray()
        triangle_id_array.SetArray(mesh.triangles, mesh.triangle_count*4, True)
        triangles.SetCells(mesh.triangle_count, triangle_id_array)

        # remember we got the alpha channel!
        specular_color = mesh.specular_color
        diffuse_color = mesh.diffuse_color

        mesh_poly_data = vtk.vtkPolyData()
        mesh_poly_data.SetPoints(vertices)
        mesh_poly_data.SetPolys(triangles)

        super().__init__(mesh_poly_data)
        self.default_opacity = opacity
        self.default_color_specular = specular_color
        self.default_color_diffuse = diffuse_color
        self.reset_opacity()
        self.reset_color_specular()
        self.reset_color_diffuse()

        logging.info('processed mesh containing {} vertices and {} triangles in: {:.3}s'
                     .format(mesh.vertex_count, mesh.triangle_count, time.time() - start))
