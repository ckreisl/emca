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

from PySide2.QtWidgets import QWidget
import abc


class Plugin(QWidget):
    """
    Plugin interface, inherits from QWidget

    The plugin interface can be used to visualizes own generated data sets.
    It can request own data from the server interface or work on the current render data,
    to visualize other aspects which are not implemented yet.

    New plugins are loaded via Plugins/__init__.py,
    therefore import new plugins there and add the class name to __all__ list.
    """

    def __init__(self, name, flag):
        QWidget.__init__(self, parent=None)
        self._name = name
        self._flag = flag
        self._scene_renderer = None

    @property
    def flag(self):
        """
        Returns the unique identifier of the plugin
        :return: flag (unique identifier)
        """
        return self._flag

    @property
    def name(self):
        """
        Returns the name of the plugin
        :return: plugin name
        """
        return self._name

    @property
    def scene_renderer(self):
        """
        Return the renderer
        Allows plugin full control of renderer
        Plugin itself has to handle add / remove of items
        """
        return self._scene_renderer

    @scene_renderer.setter
    def scene_renderer(self, scene_renderer):
        """
        Sets the renderer
        Allows plugin full control of renderer
        Plugin itself has to handle add / remove of items
        """
        self._scene_renderer = scene_renderer

    def send_update_path_indices(self, indices, add_item):
        """
        This function gets overwritten by the plugin view container,
        which will connect this function with the controller
        :param indices: numpy array:
        :param add_item: bool, add values or not:
        :return:
        """

    def send_select_path(self, index):
        """
        This function gets overwritten by the plugin view container,
        which will connect this function with the controller
        :param index:
        :return:
        """
        pass

    def send_select_vertex(self, tpl):
        """
        This function gets overwritten by the plugin view container,
        which will connect this function with the controller
        :param tpl:
        :return:
        """
        pass

    @abc.abstractmethod
    def apply_theme(self, theme):
        """
        Apply the current theme 'light' | 'dark' to the plugins view
        :param: theme (dark|light)
        :return:
        """
        pass

    @abc.abstractmethod
    def init_render_data(self, render_data):
        """
        Apply current pixel render data to plugins
        :param render_data:
        :return:
        """
        pass

    @abc.abstractmethod
    def prepare_new_data(self):
        """
        Resets all views and prepares class for new incoming pixel data package
        :return:
        """
        pass

    @abc.abstractmethod
    def update_path_indices(self, indices):
        """
        Sends list of path indices to all views to update selected paths
        :param indices: Numpy array [(path_index),...]
        :return:
        """
        pass

    @abc.abstractmethod
    def update_vertex_indices(self, tpl_list):
        """
        Send update of multiple selected vertices as tuple list
        :param tpl_list: [(path_index, vertex_index), ...]
        :return:
        """
        pass

    @abc.abstractmethod
    def select_path(self, index):
        """
        Will be called if a path element is selected within the view
        :param index: path_idx
        :return:
        """
        pass

    @abc.abstractmethod
    def select_vertex(self, tpl):
        """
        Will be called if a vertex element is selected within the view
        :param tpl: (path_idx, vertex_idx)
        :return:
        """
        pass

    @abc.abstractmethod
    def serialize(self, stream):
        """
        Send data to server
        :param stream:
        :return:
        """
        pass

    @abc.abstractmethod
    def deserialize(self, stream):
        """
        Receive data from server
        Will be handled within an extra thread,
        therefor do not update Qt view elements within this function
        :param stream:
        :return:
        """
        pass

    @abc.abstractmethod
    def update_view(self):
        """
        This function will be called after deserialize is finished
        It will update all data within the view
        :return:
        """
