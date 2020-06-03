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

from Types.color3 import Color3f
import vtk
import logging


class Shape(vtk.vtkActor):

    def __init__(self,
                 mesh_poly_data,
                 default_opacity=1.0,
                 default_size=1.0,
                 default_color=Color3f(1, 1, 1),
                 default_color_diffuse=Color3f(1, 1, 1),
                 default_color_specular=Color3f(0, 0, 0),
                 color_selected=Color3f(0, 1, 0)):
        super(vtk.Actor, self).__init__()
        self.default_color = default_color
        self.default_color_diffuse = default_color_diffuse
        self.default_color_specular = default_color_specular
        self.default_opacity = default_opacity
        self.default_size = default_size
        self.color_selected = color_selected
        self.is_selected = False

        # mapper
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(mesh_poly_data)
        else:
            mapper.SetInputData(mesh_poly_data)

        self.SetMapper(mapper)
        self.init_default_properties()

    def init_default_properties(self):
        """
        Initialise the properties
        :return:
        """
        self.GetProperty().SetLighting(True)
        self.GetProperty().LightingOn()
        self.GetProperty().SetShading(True)
        self.GetProperty().ShadingOn()
        self.GetProperty().SetDiffuseColor(self.default_color_diffuse.red,
                                           self.default_color_diffuse.green,
                                           self.default_color_diffuse.blue)
        self.GetProperty().SetSpecularColor(self.default_color_specular.red,
                                            self.default_color_specular.green,
                                            self.default_color_specular.blue,)
        self.GetProperty().SetDiffuse(1)
        self.GetProperty().SetSpecular(1)
        self.GetProperty().SetAmbient(0)
        self.GetProperty().SetOpacity(self.default_opacity)

    def set_selected(self, selected):
        """
        Highlight the mesh object as selected
        :param selected: boolean
        :return:
        """
        if selected:
            self.GetProperty().SetColor(self.color_selected.red,
                                        self.color_selected.green,
                                        self.color_selected.blue)
        else:
            self.GetProperty().SetColor(self.default_color.red,
                                        self.default_color.green,
                                        self.default_color.blue)
        self.is_selected = selected

    def set_selected_color(self, color):
        """
        Set the color if the items gets selected
        :param: Color3f
        """
        self.color_selected = color

    def get_size(self):
        """
        Return vtkGetPointSize of object
        :return: float
        """
        return self.GetProperty().GetPointSize()

    def get_default_size(self):
        """
        Returns default set object size
        :return: float
        """
        return self.default_size

    def set_size(self, size):
        """
        Sets the size of the object
        :param size: float
        """
        self.GetProperty().SetPointSize(size)

    def get_opacity(self):
        return self.GetProperty.GetOpacity()

    def get_default_opacity(self):
        return self.default_opacity

    def get_color(self):
        return self.GetProperty().GetColor()

    def get_default_color(self):
        return self.default_color

    def set_color(self, color):
        if isinstance(color, list):
            self.GetProperty.SetColor(color)
        elif isinstance(color, Color3f):
            self.GetProperty.SetColor(color.to_list_rgb())

    def set_color_rgb(self, r, g, b):
        self.GetProperty.SetColor([r, g, b])

    def get_color_diffuse(self):
        return self.GetProperty().GetDiffuseColor()

    def get_default_color_diffuse(self):
        return self.default_color_diffuse

    def set_color_diffuse(self, color_diffuse):
        if isinstance(color_diffuse, list):
            self.GetProperty.SetDiffuseColor(color_diffuse)
        elif isinstance(color_diffuse, Color3f):
            self.GetProperty.SetDiffuseColor(color_diffuse.to_list_rgb())

    def get_color_specular(self):
        return self.GetProperty().GetSpecularColor()

    def get_default_color_specular(self):
        return self.default_color_specular

    def set_color_specular(self, color_specular):
        if isinstance(color_specular, list):
            self.GetProperty.SetSpecularColor(color_specular)
        elif isinstance(color_specular, Color3f):
            self.GetProperty.SetSpecularColor(color_specular.to_list_rgb())

    def reset_size(self):
        self.GetProperty.SetPointSize(self.default_size)

    def reset_opacity(self):
        self.GetProperty.SetOpacity(self.default_opacity)

    def reset_color(self):
        self.GetProperty.SetColor(self.default_color.to_list_rgb())

    def reset_color_diffuse(self):
        self.GetProperty.SetColor(self.default_color_diffuse.to_list_rgb())

    def reset_color_specular(self):
        self.GetProperty.SetColor(self.default_color_specular.to_list_rgb())

    def reset_all(self):
        self.reset_size()
        self.reset_opacity()
        self.reset_color()
        self.reset_color_diffuse()
        self.reset_color_specular()

