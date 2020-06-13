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
import abc
import logging


class SceneInterface(object):

    """
    Interface which defines all scene functionalities which the view provides at the moment.
    This needs to be implemented in case you want to change the current used vtk renderer
    """

    def __init__(self):
        self.view_render_scene = None
        self.view_render_scene_options = None

    def set_view_render_scene(self, view_render_scene):
        self.view_render_scene = view_render_scene

    def set_view_render_scene_options(self, view_render_scene_options):
        self.view_render_scene_options = view_render_scene_options

    def send_update_path(self, indices, add_item):
        self.view_render_scene.send_update_path(indices, add_item)

    def send_select_path(self, index):
        self.view_render_scene.send_select_path(index)

    def send_select_vertex(self, tpl):
        self.view_render_scene.send_select_vertex(tpl)

    @property
    @abc.abstractmethod
    def widget(self):
        """
        Returns the corresponding 3D scene render QtWidget
        :return:
        """

    @abc.abstractmethod
    def get_path_option_settings(self, index):
        """
        Returns the path option settings of one path defined by its index
        :param index: integer
        :return: dict
        """

    @abc.abstractmethod
    def get_vertex_option_settings(self, tpl):
        """
        Returns the vertex option settings defined by its tpl (path_index, vertex_index)
        :param: tuple (path_index, vertex_index)
        :return: dict
        """

    @abc.abstractmethod
    def get_camera_option_settings(self):
        """
        Returns the options settings of the camera
        :return: dict
        """

    @abc.abstractmethod
    def get_scene_option_settings(self):
        """
        Returns the options settings of the scene
        :return: dict
        """

    @abc.abstractmethod
    def update_path_indices(self, indices):
        """
        Update of current selected path key indices
        :param: numpy array containing path indices
        :return:
        """

    @abc.abstractmethod
    def select_path(self, index):
        """
        Select and highlight one path if other paths are active in parallel decrease opacity
        :param: integer index
        :return:
        """

    @abc.abstractmethod
    def select_vertex(self, tpl):
        """
        Informs the renderer to select / highlight the vertex - Tuple (path_index, vertex_index)
        :param tpl: tuple(path_index, vertex_index)
        :return:
        """

    @abc.abstractmethod
    def load_scene(self, camera_data, mesh_data):
        """
        Loads the 3D rendered scene.
        Containing information about the camera and all scene objects.
        :param camera_data: Model Camera Data
        :param mesh_data: Model Mesh Data
        :return:
        """

    @abc.abstractmethod
    def load_camera(self, camera_data):
        """
        Loads the 3D camera from provided camera settings from the render system server
        :param camera_data: Model Camera Data
        :return:
        """

    @abc.abstractmethod
    def load_mesh(self, mesh_data):
        """
        Loads one mesh objects provided by the render system server
        :param: Model Mesh Data
        :return:
        """

    @abc.abstractmethod
    def load_traced_paths(self, render_data):
        """
        Creates and loads the 3D path objects from the render data sent by the render system server
        :param: Model Render Data
        :return:
        """

    @abc.abstractmethod
    def display_traced_paths(self, indices):
        """
        Informs the renderer to display all path which are in the indices list
        :param indices: numpy array containing path indices
        :return:
        """

    @abc.abstractmethod
    def clear_scene_objects(self):
        """
        Removes all 3D scene objects from the scene
        :return:
        """

    @abc.abstractmethod
    def clear_traced_paths(self):
        """
        Removes all traced paths within the scene
        :return:
        """

    @abc.abstractmethod
    def reset_camera_position(self):
        """
        Resets the 3D camera position to it's default initialized position
        :return:
        """

    @abc.abstractmethod
    def prepare_new_data(self):
        """
        Prepare 3D scene for new incoming selected pixel data from render system server
        :return:
        """

    # SCENE OPTIONS

    @abc.abstractmethod
    def apply_camera_option_settings(self, camera_settings):
        """
        Apply camera option changes from the scene option view
        :param camera_settings: dict
        :return:
        """

    @abc.abstractmethod
    def reset_camera_option_settings(self):
        """
        Resets the camera option settings to its default values
        :return:
        """

    @abc.abstractmethod
    def apply_scene_option_settings(self, scene_settings):
        """
        Apply scene option changes from the scene option view
        :param scene_settings: dict
        :return:
        """

    @abc.abstractmethod
    def reset_scene_option_settings(self):
        """
        Resets the scene option settings to its default values
        :return:
        """

    @abc.abstractmethod
    def show_all_other_traced_paths(self, enable):
        """
        Depending on input show all traced paths within the 3d scene
        :param enable: boolean
        :return:
        """

    @abc.abstractmethod
    def show_all_other_traced_vertices(self, enable):
        """
        Depending on input show all traced vertices within the 3d scene
        :param enable: boolean
        :return:
        """

    @abc.abstractmethod
    def show_traced_path(self, path_index, enable):
        """
        Depending on input enable or disable current select path
        :param path_index: integer
        :param enable: boolean
        :return:
        """

    @abc.abstractmethod
    def update_path_opacity(self, path_index, opacity):
        """
        Updated the current selected path opacity
        :param path_index: integer
        :param opacity: float
        :return:
        """

    @abc.abstractmethod
    def update_path_size(self, path_index, size):
        """
        Updated the current selected path size
        :param path_index: integer
        :param size: float
        :return:
        """

    @abc.abstractmethod
    def reset_path(self, path_index):
        """
        Resets opacity and size of the selected path
        :param path_index: integer
        :return:
        """

    @abc.abstractmethod
    def show_all_traced_vertices(self, state):
        """
        Depending on input shows all intersections within the 3d scene
        :param state: boolean
        :return:
        """

    @abc.abstractmethod
    def update_vertex_opacity(self, vertex_tpl, opacity):
        """
        Updates the vertex opacity
        :param vertex_tpl: (path_index, vertex_index)
        :param opacity: float
        :return:
        """

    @abc.abstractmethod
    def update_vertex_size(self, vertex_tpl, size):
        """
        Updates the vertex size
        :param vertex_tpl: (path_index, vertex_index)
        :param size: float
        :return:
        """

    @abc.abstractmethod
    def reset_vertex(self, vertex_tpl):
        """
        Resets opacity and size of the selected vertex
        :param vertex_tpl: (path_index, vertex_index)
        :return:
        """

    @abc.abstractmethod
    def show_all_traced_nees(self, enabled):
        """
        Displays all next event estimations in the 3d scene
        :param enabled: boolean
        :return:
        """

    @abc.abstractmethod
    def show_traced_path_nee(self, path_index, enabled):
        """
        Displays the next event estimations rays of the current selected path
        :param path_index: integer
        :param enabled: boolean
        :return:
        """

    @abc.abstractmethod
    def show_vertex_omega_o(self, vertex_tpl, enabled):
        """
        Displays the outgoing ray of the current selected vertex / intersection
        :param vertex_tpl: (path_index, vertex_index)
        :param enabled: boolean
        :return:
        """

    @abc.abstractmethod
    def show_vertex_omega_i(self, vertex_tpl, enabled):
        """
        Displays the incoming ray of the current selected vertex / intersection
        :param vertex_tpl: (path_index, vertex_index)
        :param enabled: boolean
        :return:
        """

    @abc.abstractmethod
    def show_vertex_nee(self, vertex_tpl, enabled):
        """
        Displays the next event estimation ray of the current selected vertex / intersection
        :param vertex_tpl: (path_index, vertex_index)
        :param enabled: boolean
        :return:
        """

    @abc.abstractmethod
    def reset_all_paths_vertices(self):
        """
        Resets the opacity and size of all paths and its intersections
        :return:
        """

    # BASIC SHAPES

    @abc.abstractmethod
    def draw_triangle(self, p1, p2, p3):
        """
        Draws a triangle in the 3d scene.
        Users has to take care of object
        :param p1: Point3f
        :param p2: Point3f
        :param p3: Point3f
        :return: SceneObject
        """

    @abc.abstractmethod
    def draw_sphere(self, center, radius):
        """
        Draws a triangle in the 3d scene.
        Users has to take care of object
        :param center: Point3f
        :param radius: float
        :return: SceneObject
        """

    @abc.abstractmethod
    def draw_line(self, p1, p2):
        """
        Draws a triangle in the 3d scene.
        Users has to take care of object
        :param p1: Point3f
        :param p2: Point3f
        :return: SceneObject
        """

    @abc.abstractmethod
    def draw_point(self, p1):
        """
        Draws a triangle in the 3d scene.
        Users has to take care of object
        :param p1: Point3f
        :return: SceneObject
        """

    @abc.abstractmethod
    def remove_object(self, obj):
        """
        Removed the object from the scene renderer
        :param obj: SceneObject
        :return: boolean
        """
