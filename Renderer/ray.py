"""
    This file is part of EMCA, an explorer of Monte-Carlo based Algorithms.
    Copyright (c) 2019-2020 by Christoph Kreisl and others.
    EMCA is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License Version 3
    as published by the Free Software Foundation.
    EMCA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
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

    def create_arrow(self, start_pos, end_pos, is_ne, is_ne_occluded, is_envmap):

        start_pos = list(start_pos)
        end_pos = list(end_pos)

        # Create an arrow.
        arrowSource = vtk.vtkArrowSource()
        """
        arrowSource.SetShaftRadius(0.003)
        arrowSource.SetShaftResolution(20)
        arrowSource.SetTipLength(0.03)
        arrowSource.SetTipResolution(20)
        arrowSource.SetTipRadius(0.0055)
        """

        # Generate a random start and end point
        random.seed(8775070)
        # Compute a basis
        normalizedX = [0 for i in range(3)]
        normalizedY = [0 for i in range(3)]
        normalizedZ = [0 for i in range(3)]

        # The X axis is a vector from start to end
        math = vtk.vtkMath()
        math.Subtract(end_pos, start_pos, normalizedX)
        math.Normalize(normalizedX)

        # The Z axis is an arbitrary vector cross X
        arbitrary = [0 for i in range(3)]
        arbitrary[0] = random.uniform(-10, 10)
        arbitrary[1] = random.uniform(-10, 10)
        arbitrary[2] = random.uniform(-10, 10)
        math.Cross(normalizedX, arbitrary, normalizedZ)
        math.Normalize(normalizedZ)

        # The Y axis is Z cross X
        math.Cross(normalizedZ, normalizedX, normalizedY)
        matrix = vtk.vtkMatrix4x4()

        # Create the direction cosine matrix
        matrix.Identity()
        for i in range(3):
            matrix.SetElement(i, 0, normalizedX[i])
            matrix.SetElement(i, 1, normalizedY[i])
            matrix.SetElement(i, 2, normalizedZ[i])

        # Apply the transforms
        transform = vtk.vtkTransform()
        transform.Translate(start_pos)
        transform.Concatenate(matrix)

        # Transform the polydata
        transformPD = vtk.vtkTransformPolyDataFilter()
        transformPD.SetTransform(transform)
        transformPD.SetInputConnection(arrowSource.GetOutputPort())

        # Create a mapper and actor for the arrow
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(transformPD.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # mark rays which are next event estimations
        if is_ne:
            if is_ne_occluded:
                actor.GetProperty().SetColor(1.0, 0.0, 0.0)
            else:
                actor.GetProperty().SetColor(0.0, 0.0, 1.0)

        # mark rays which hit the envmap
        if is_envmap:
            actor.GetProperty().SetColor(1.0, 1.0, 0.0)

        return actor

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
