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
        """

    @abc.abstractmethod
    def reset_camera_option_settings(self):
        """
        Resets the camera option settings to its default values
        """

    @abc.abstractmethod
    def apply_scene_option_settings(self, scene_settings):
        """
        Apply scene option changes from the scene option view
        """

    @abc.abstractmethod
    def reset_scene_option_settings(self):
        """
        Resets the scene option settings to its default values
        """

    @abc.abstractmethod
    def apply_path_option_settings(self, path_settings):
        """
        Apply path option changes from the scene option view
        """

    @abc.abstractmethod
    def reset_path_option_settings(self):
        """
        Resets the path option settings to its default values
        """

    @abc.abstractmethod
    def apply_vertex_option_settings(self, vertex_settings):
        """
        Apply path option changes from the scene option view
        """

    @abc.abstractmethod
    def reset_vertex_option_settings(self):
        """
        Resets the vertex option settings to its default values
        """