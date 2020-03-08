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
