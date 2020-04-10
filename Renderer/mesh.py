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
import logging
import time


class Mesh(vtk.vtkActor):

    """
        Mesh
        Represents a Mesh object within the 3D scene as vtkActor
    """

    def __init__(self, mesh, opacity):
        vtk.vtkActor.__init__(self)

        self._default_opacity = opacity
        self._is_selected = False

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

        self.init_mapper(vertices, triangles)
        self.init_properties(diffuse_color, specular_color)

        self._default_color = self.GetProperty().GetColor()

        logging.info('processed mesh containing {} vertices and {} triangles in: {:.3}s'
                     .format(mesh.vertex_count, mesh.triangle_count, time.time() - start))

    @property
    def is_selected(self):
        """
        Returns if the mesh is selected
        :return: boolean
        """
        return self._is_selected

    def init_mapper(self, vertices, triangles):
        """
        Initialise the mesh (vtkActor)
        :param vertices:
        :param triangles:
        :return:
        """
        # mesh poly data
        mesh_poly_data = vtk.vtkPolyData()
        mesh_poly_data.SetPoints(vertices)
        mesh_poly_data.SetPolys(triangles)

        # mapper
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(mesh_poly_data)
        else:
            mapper.SetInputData(mesh_poly_data)

        self.SetMapper(mapper)

    def init_properties(self, diffuse_color, specular_color):
        """
        Initialise the properties
        :param diffuse_color:
        :param specular_color:
        :return:
        """
        self.GetProperty().SetLighting(True)
        self.GetProperty().LightingOn()
        self.GetProperty().SetShading(True)
        self.GetProperty().ShadingOn()
        self.GetProperty().SetDiffuseColor(diffuse_color[0], diffuse_color[1], diffuse_color[2])
        self.GetProperty().SetSpecularColor(specular_color[0], specular_color[1], specular_color[2])
        self.GetProperty().SetDiffuse(1)
        self.GetProperty().SetSpecular(1)
        self.GetProperty().SetAmbient(0)
        self.GetProperty().SetOpacity(self._default_opacity)

    def set_selected(self, selected):
        """
        Highlight the mesh object as selected
        :param selected: boolean
        :return:
        """
        if selected:
            self.GetProperty().SetColor(0.3, 0, 0.2)
        else:
            self.GetProperty().SetColor(self._default_color)
        self._is_selected = selected

    @property
    def opacity(self):
        """
        Returns the opacity of the mesh object
        :return: float[0,1]
        """
        return self.GetProperty().GetOpacity()

    @property
    def color(self):
        """
        Returns the color of the mesh object
        :return: vtkColor
        """
        return self.GetProperty().GetColor()

    @property
    def default_opacity(self):
        """
        Returns the default opacity value 1.0
        :return:
        """
        return self._default_opacity

    def set_opacity(self, value):
        """
        Sets the opacity of the mesh object
        :param value: float[0,1]
        :return:
        """
        self.GetProperty().SetOpacity(value)

    def set_color(self, color):
        """
        Sets the color of the mesh object
        :param color: vtkColor
        :return:
        """
        self.GetProperty().SetColor(color)

    def reset(self):
        """
        Resets the mesh opacity and color to default
        :return:
        """
        if self.is_selected:
            self.GetProperty().SetColor(self._default_color)
        self.GetProperty().SetOpacity(self._default_opacity)
        self._is_selected = False
