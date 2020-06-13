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

from Renderer.rubberband import RubberBandInteractor
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from Renderer.path_vertex import PathVertex
from Renderer.line import Line
from Renderer.sphere import Sphere
from Renderer.triangle import Triangle
from PySide2.QtWidgets import QFrame
import vtk
import logging


class Renderer(vtk.vtkRenderer):

    """
        Renderer
        Represents the render which visualizes all 3D objects within the 3D viewer
        A vtkRenderer is used.
    """

    def __init__(self):
        super().__init__()
        # widget
        self._frame = QFrame()
        self._vtkWidget = QVTKRenderWindowInteractor(self._frame)

        # renderer
        self.SetBackground(0.7, 0.7, 0.7)

        # Overall scene light
        light_kit = vtk.vtkLightKit()
        light_kit.SetKeyLightIntensity(1.0)
        light_kit.SetKeyLightWarmth(0.5)
        light_kit.AddLightsToRenderer(self)

        self._vtkWidget.GetRenderWindow().AddRenderer(self)
        self._iren = self._vtkWidget.GetRenderWindow().GetInteractor()

        style = RubberBandInteractor(parent=self)
        style.SetDefaultRenderer(self)
        self._iren.SetInteractorStyle(style)

        # set picket to allow rubber band picker (rectangle 3D selection)
        area_picker = vtk.vtkAreaPicker()
        area_picker.AddObserver(vtk.vtkCommand.EndPickEvent, self.area_picker_event)

        self._rubber_band_callback = None

        self._iren.SetPicker(area_picker)
        self._iren.Initialize()
        self._iren.Start()

    @property
    def widget(self):
        """
        Returns the widget containing the renderer view
        :return: vtkWidget
        """
        return self._vtkWidget

    def set_rubber_band_callback(self, callback):
        """
        Sets the rubber band callback function.
        Informs the scene renderer about picked items
        :param callback: function
        :return:
        """
        self._rubber_band_callback = callback

    def area_picker_event(self, picker, event):
        """
        Handles the rubber band selector,
        check if items gets selected and informs the controller about it
        :param picker:
        :param event:
        :return:
        """
        props = picker.GetProp3Ds()
        props.InitTraversal()
        picked = props.GetNumberOfItems()
        for i in range(0, picked):
            prop = props.GetNextProp3D()
            if isinstance(prop, PathVertex):
                tpl = prop.get_index_tpl()
                # TODO check case if callback function is none
                self._rubber_band_callback(tpl)
                break

    # plugin functions
    def draw_triangle(self, p1, p2, p3):
        """
        Draws a triangle in the 3D scene
        :param p1: Point3f
        :param p2: Point3f
        :param p3: Point3f
        :return: vtkActor
        """
        obj = Triangle(p1, p2, p3)
        self.AddActor(obj)
        self._vtkWidget.update()
        return obj

    def draw_sphere(self, center, radius):
        """
        Draws a sphere in the 3D scene with given radius
        :param center: Point3f
        :param radius: float
        :return: vtkActor
        """
        obj = Sphere(center, radius)
        self.AddActor(obj)
        self._vtkWidget.update()
        return obj

    def draw_line(self, start_pos, end_pos):
        """
        Draws a line in the 3D scene
        :param start_pos: Point3f
        :param end_pos: Point3f
        :return: vtkActor
        """
        obj = Line(start_pos, end_pos)
        self.AddActor(obj)
        self._vtkWidget.update()
        return obj

    def draw_point(self, pos):
        """
        Draws a point / vertex in the 3D scene
        :param pos: Point3f
        :return: vtkActor
        """
        pass
