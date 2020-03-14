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

from Model.mesh_data import Mesh
import vtk
import logging


class MouseInteractor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        vtk.vtkInteractorStyleTrackballCamera.__init__(self)

        self._view_render_scene = parent
        self._curActor = None

        self.AddObserver("LeftButtonPressEvent", self.left_btn_press_event)
        self.AddObserver("LeftButtonReleaseEvent", self.left_btn_release_event)
        self.AddObserver("KeyPressEvent", self.key_press_event)

    def key_press_event(self, obj, event):
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

    def left_btn_press_event(self, obj, event):
        click_pos = self.GetInteractor().GetEventPosition()
        picker = vtk.vtkPropPicker()
        picker.Pick(click_pos[0], click_pos[1], 0, self.GetDefaultRenderer())

        # get the new
        self._curActor = picker.GetActor()

        """
        if isinstance(self._curActor, Mesh):
            self._view_render_scene.update_mesh_idx(self._curActor.mesh_idx)
        """

        self.OnLeftButtonDown()

    def left_btn_release_event(self, obj, event):
        self.OnLeftButtonUp()
