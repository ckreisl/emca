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
        pass

    @abc.abstractmethod
    def load_scene(self, camera_data, mesh_data):
        """
        Loads the 3D rendered scene.
        Containing information about the camera and all scene objects.
        """
        pass

    @abc.abstractmethod
    def load_camera(self, camera_data):
        """
        Loads the 3D camera from provided camera settings from the render system server
        """
        pass

    @abc.abstractmethod
    def load_mesh(self, mesh_data):
        """
        Loads one mesh objects provided by the render system server
        """
        pass

    @abc.abstractmethod
    def load_traced_paths(self, render_data):
        """
        Creates and loads the 3D path objects from the render data sent by the render system server
        """

    @abc.abstractmethod
    def display_traced_paths(self, indices):
        """
        Informs the renderer to display all path which are in the indices list
        :param indices: numpy array containing path indices
        :return:
        """
        pass

    @abc.abstractmethod
    def clear_scene_objects(self):
        """
        Removes all 3D scene objects from the scene
        """
        pass

    @abc.abstractmethod
    def clear_traced_paths(self):
        """
        Removes all traced paths within the scene
        """
        pass

    @abc.abstractmethod
    def reset_camera_position(self):
        """
        Resets the 3D camera position to it's default initialized position
        """
        pass

    @abc.abstractmethod
    def prepare_new_data(self):
        """
        Prepare 3D scene for new incoming selected pixel data from render system server
        """
        pass
