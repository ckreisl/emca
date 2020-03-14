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
import logging


class RubberBandInteractor(vtk.vtkInteractorStyleRubberBandPick):

    """
        RubberBandInteractor
        Allows a rubber band selector by clicking the 'r' key within the 3D renderer scene view.
        The selected vertex and its corresponding path will be automatically be visualized within all other views.
        Therefore all, other rays will be removed from the scene view.
    """

    def __init__(self, parent=None):
        super().__init__()

        self.AddObserver("KeyPressEvent", self.key_press_event)

    def key_press_event(self, obj, event):
        """
        Handles key input for the 3D scene viewer.
        Moves the camera within the scene
        :param obj:
        :param event:
        :return:
        """
        key = self.GetInteractor().GetKeySym()
        camera = self.GetDefaultRenderer().GetActiveCamera()

        if key == 'Up':
            camera.move_forward()
        elif key == 'Left':
            camera.move_left()
        elif key == 'Right':
            camera.move_right()
        elif key == 'Down':
            camera.move_backward()
        elif key == '8':
            camera.move_up()
        elif key == '4':
            camera.pan_left()
        elif key == '6':
            camera.pan_right()
        elif key == '2':
            camera.move_down()

        self.GetDefaultRenderer().ResetCameraClippingRange()
        self.GetInteractor().Render()
