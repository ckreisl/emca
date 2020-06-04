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
        super().__init__()
        self._default_color = default_color
        self._default_color_diffuse = default_color_diffuse
        self._default_color_specular = default_color_specular
        self._default_opacity = default_opacity
        self._default_size = default_size
        self._color_selected = color_selected
        self._is_selected = False

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
        self.GetProperty().SetDiffuseColor(self._default_color_diffuse.red,
                                           self._default_color_diffuse.green,
                                           self._default_color_diffuse.blue)
        self.GetProperty().SetDiffuse(1)
        """
        self.GetProperty().SetSpecularColor(self._default_color_specular.red, 
                                            self._default_color_specular.green, 
                                            self._default_color_specular.blue,)        
        self.GetProperty().SetSpecular(1)
        """
        self.GetProperty().SetAmbient(0)
        self.GetProperty().SetOpacity(self._default_opacity)

    @property
    def selected(self):
        """
        Returns if the item is currently selected and highlighted
        :return: boolean
        """
        return self._is_selected

    @selected.setter
    def selected(self, selected):
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
        self._is_selected = selected

    @property
    def selected_color(self):
        """
        Returns the color if item is selected
        :return: Color3f / List
        """
        return self._color_selected

    @selected_color.setter
    def selected_color(self, color):
        """
        Set the color if the items gets selected
        :param: Color3f
        """
        self._color_selected = color

    @property
    def size(self):
        """
        Return vtkGetPointSize of object
        :return: float
        """
        return self.GetProperty().GetPointSize()

    @size.setter
    def size(self, size):
        """
        Sets the size of the object
        :param size: float
        """
        self.GetProperty().SetPointSize(size)

    @property
    def default_size(self):
        """
        Returns default set object size
        :return: float
        """
        return self._default_size

    @default_size.setter
    def default_size(self, size):
        """
        Sets the default size of the object
        :param: integer
        :return: None
        """
        self._default_size = size

    @property
    def opacity(self):
        """
        Returns the current opacity of the object
        :return: float
        """
        return self.GetProperty().GetOpacity()

    @opacity.setter
    def opacity(self, value):
        """
        Sets the opacity of the object
        :param: float
        :return: None
        """
        self.GetProperty().SetOpacity(value)

    @property
    def default_opacity(self):
        """
        Returns the default object opacity which was set
        :return: float
        """
        return self._default_opacity

    @default_opacity.setter
    def default_opacity(self, value):
        """
        Sets the default opacity of the object
        :param: float [0,1]
        """
        self._default_opacity = value

    @property
    def color(self):
        """
        Returns the actual color of the object
        :return: Color3f / list
        """
        return self.GetProperty().GetColor()

    @color.setter
    def color(self, color):
        """
        Sets the current color of the object
        :param: Color3f / list
        :return: None
        """
        if isinstance(color, list):
            self.GetProperty().SetColor(color)
        elif isinstance(color, Color3f):
            self.GetProperty().SetColor(color.to_list_rgb())

    @property
    def default_color(self):
        """
        Returns the default color of the object
        :return: Color3f
        """
        return self._default_color

    @default_color.setter
    def default_color(self, color):
        """
        Sets the default color of the object
        :param: Color3f
        :return: None
        """
        self._default_color = color

    def set_color_rgb(self, r, g, b):
        """
        Sets the color of the actual object
        """
        self.GetProperty().SetColor([r, g, b])

    @property
    def color_diffuse(self):
        """
        Returns the current diffuse color of the object
        :return: Color3f
        """
        return self.GetProperty().GetDiffuseColor()

    @color_diffuse.setter
    def color_diffuse(self, color_diffuse):
        """
        Sets the diffuse color of the object
        :param: Color3f / list
        :return: None
        """
        if isinstance(color_diffuse, list):
            self.GetProperty().SetDiffuseColor(color_diffuse)
        elif isinstance(color_diffuse, Color3f):
            self.GetProperty().SetDiffuseColor(color_diffuse.to_list_rgb())

    @property
    def default_color_diffuse(self):
        """
        Get the default diffuse color of the object
        :return: Color3f
        """
        return self._default_color_diffuse

    @default_color_diffuse.setter
    def default_color_diffuse(self, color):
        """
        Sets the default diffuse color of the object
        :param: Color3f
        """
        self._default_color_diffuse = color

    @property
    def color_specular(self):
        """
        Return the current specular color of the object
        :return: list
        """
        return self.GetProperty().GetSpecularColor()

    @color_specular.setter
    def color_specular(self, color_specular):
        """
        Sets the specular color of the object
        :param: Color3f / list
        :return: None
        """
        if isinstance(color_specular, list):
            self.GetProperty.SetSpecularColor(color_specular)
        elif isinstance(color_specular, Color3f):
            self.GetProperty.SetSpecularColor(color_specular.to_list_rgb())

    @property
    def default_color_specular(self):
        """
        Return the default specular color of the object
        :return: Color3f
        """
        return self.default_color_specular

    @default_color_specular.setter
    def default_color_specular(self, color):
        """
        Sets the default specular color of the object
        """
        self._default_color_specular = color

    def reset_size(self):
        """
        Resets the size to the set default value
        """
        self.GetProperty().SetPointSize(self._default_size)

    def reset_opacity(self):
        """
        Resets the opacity to the set default value
        """
        self.GetProperty().SetOpacity(self._default_opacity)

    def reset_color(self):
        """
        Resets the object color to the set default value
        """
        self.GetProperty().SetColor(self._default_color.to_list_rgb())

    def reset_color_diffuse(self):
        """
        Resets the objects diffuse color to the default value which is set
        """
        self.GetProperty().SetColor(self._default_color_diffuse.to_list_rgb())

    def reset_color_specular(self):
        """
        Resets the objects specular color to the default value which is set
        """
        self.GetProperty().SetColor(self._default_color_specular.to_list_rgb())

    def reset_all(self):
        """
        Reset everything, size, opacity, color, diffuse color, specular color
        Everything will be reseted to the provided default value.
        """
        self.reset_size()
        self.reset_opacity()
        self.reset_color()
        self.reset_color_diffuse()
        self.reset_color_specular()

