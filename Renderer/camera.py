import vtk


class Camera(vtk.vtkCamera):

    """
        Camera
        Represents a modified vtkCamera class for the 3D viewer
    """

    def __init__(self, camera_data):
        vtk.vtkCamera.__init__(self)

        # boolean to check if camera should always set the viewing direction to selected vertex
        self._auto_clipping = True
        self._speed = 1.0
        # save parameters for camera reset
        self._origin = camera_data.origin
        self._focal_point = camera_data.direction
        self._up = camera_data.up
        self._near_clip = camera_data.near_clip
        self._far_clip = camera_data.far_clip
        self._focus_dist = camera_data.focus_dist
        self._fov = camera_data.fov

        self.reset()

    def reset(self):
        """
        Resets the camera settings to its default values
        :return:
        """
        self.SetPosition(self._origin.x,
                         self._origin.y,
                         self._origin.z)
        self.SetFocalPoint(self._focal_point.x,
                           self._focal_point.y,
                           self._focal_point.z)
        self.SetViewUp(self._up.x,
                       self._up.y,
                       self._up.z)
        self.SetClippingRange(self._near_clip,
                              self._far_clip)
        self.SetDistance(self._focus_dist)
        self.SetViewAngle(self._fov)

    @property
    def auto_clipping(self):
        """
        Returns if auto clipping is enabled or disabled
        :return: boolean
        """
        return self._auto_clipping

    @auto_clipping.setter
    def auto_clipping(self, new_value):
        """
        Setter function, sets the auto clipping value
        :param new_value: boolean
        :return:
        """
        self._auto_clipping = new_value

    @property
    def motion_speed(self):
        """
        Returns the camera motion speed
        :return:
        """
        return self._speed

    @motion_speed.setter
    def motion_speed(self, new_value):
        """
        Setter function, sets the camera motion speed
        :param new_value:
        :return:
        """
        self._speed = new_value

    def set_focal_point(self, focal_p):
        """
        Sets the focal point of the camera
        :param focal_p: list[x,y,z]
        :return:
        """
        self.SetFocalPoint(focal_p[0], focal_p[1], focal_p[2])

    def reset_motion_speed(self):
        """
        Resets the camera motion speed to 1.0
        :return:
        """
        self._speed = 1.0

    def pan_left(self):
        """
        Pan camera to the left
        :return:
        """
        self.Yaw(self._speed)

    def pan_right(self):
        """
        Pan camera to the right
        :return:
        """
        self.Yaw(-self._speed)

    def move_up(self):
        """
        Move camera up
        :return:
        """
        self._motion_along_vector(self.GetViewUp(), -self._speed)

    def move_down(self):
        """
        Move camera down
        :return:
        """
        self._motion_along_vector(self.GetViewUp(), self._speed)

    def move_right(self):
        """
        Move camera right
        :return:
        """
        self._motion_along_vector(self._get_rl_vector(), -self._speed)

    def move_left(self):
        """
        Move camera left
        :return:
        """
        self._motion_along_vector(self._get_rl_vector(), self._speed)

    def move_forward(self):
        """
        Move camera forward
        :return:
        """
        self._motion_along_vector(self.GetDirectionOfProjection(), -self._speed)

    def move_backward(self):
        """
        Move camera backward
        :return:
        """
        self._motion_along_vector(self.GetDirectionOfProjection(), self._speed)

    def _get_rl_vector(self):
        """
        Returns the right-left vector of the camera
        :return:
        """
        vtm = self.GetViewTransformMatrix()
        x = vtm.GetElement(0, 0)
        y = vtm.GetElement(0, 1)
        z = vtm.GetElement(0, 2)
        return [x, y, z]

    def _motion_along_vector(self, vec, speed):
        """
        Applies a motion along a vector with given speed
        :param vec:
        :param speed:
        :return:
        """
        old_pos = self.GetPosition()
        focal_point = self.GetFocalPoint()
        self.SetPosition(
            old_pos[0] - speed * vec[0],
            old_pos[1] - speed * vec[1],
            old_pos[2] - speed * vec[2]
        )
        self.SetFocalPoint(
            focal_point[0] - speed * vec[0],
            focal_point[1] - speed * vec[1],
            focal_point[2] - speed * vec[2]
        )