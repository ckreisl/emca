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
