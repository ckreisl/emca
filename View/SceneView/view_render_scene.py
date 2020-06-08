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

from Core.messages import ViewMode
from View.SceneView.view_render_scene_options import ViewRenderSceneOptions
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QWidget
from Core.pyside2_uic import loadUi
import os
import logging


class ViewRenderScene(QWidget):

    """
        ViewRenderScene
        Handles the three-dimensional visualization.
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        ui_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ui', 'render_scene.ui'))
        loadUi(ui_filepath, self)

        self._controller = None
        self._scene_renderer = None
        self._view_render_options = ViewRenderSceneOptions()

        self._scene_loaded = False

        self.btnSceneOptions.clicked.connect(self.open_view_render_options)
        self.btnLoadScene.clicked.connect(self.request_scene)
        self.btnReset.clicked.connect(self.reset_camera_position)

    @property
    def view_render_scene_options(self):
        return self._view_render_options

    def init_scene_renderer(self, scene_renderer):
        self._scene_renderer = scene_renderer
        self._view_render_options.init_scene_renderer(scene_renderer)
        self.sceneLayout.addWidget(scene_renderer.widget)

    def set_controller(self, controller):
        """
        Sets the connection to the controller
        :param controller: Controller
        :return:
        """
        self._controller = controller

    def update_path_indices(self, indices):
        """
        Updates the view with given path indices keys from controller
        """
        self._scene_renderer.update_path_indices(indices)

    @Slot(bool, name='open_view_render_options')
    def open_view_render_options(self, clicked):
        """
        Opens the view render options
        :param clicked: boolean
        :return: boolean
        """
        if self._view_render_options.isVisible():
            self._view_render_options.activateWindow()
        else:
            self._view_render_options.show()

    @Slot(bool, name='request_scene')
    def request_scene(self, clicked):
        """
        Informs the controller to request the 3D scene data from the server
        :param clicked: boolean
        :return:
        """
        self._controller.request_scene_data()

    @Slot(bool, name='reset_camera_position')
    def reset_camera_position(self, clicked):
        """
        Informs the renderer to reset the scenes camera view
        :param clicked: boolean
        :return:
        """
        self._scene_renderer.reset_camera_position()

    def enable_view(self, enabled, mode=ViewMode.CONNECTED):
        """
        Enables the view elements depending on the ViewMode
        :param enabled: boolean
        :param mode: ViewMode
        :return:
        """
        if mode is ViewMode.CONNECTED:
            self.btnLoadScene.setEnabled(enabled)
            self.btnReset.setEnabled(enabled)
            self.btnSceneOptions.setEnabled(enabled)

    def prepare_new_data(self):
        """
        Prepare new incoming data, informs the renderer that new data is coming
        :return:
        """
        #self._view_render_options.prepare_new_data()
        self._scene_renderer.prepare_new_data()

    def clear_scene_objects(self):
        """
        Informs the renderer to clear all objects within the scene
        :return:
        """
        self._scene_renderer.clear_scene_objects()
        self._scene_loaded = False

    def load_camera(self, camera_data):
        """
        Informs the renderer about the camera data,
        loads the camera data and enables the camera settings
        :param camera_data:
        :return:
        """
        self._scene_renderer.load_camera(camera_data)
        camera_settings = self._scene_renderer.get_camera_option_settings()
        self._view_render_options.load_camera_settings(camera_settings)
        self._view_render_options.set_camera_settings_enabled(True)

    def load_mesh(self, mesh_data):
        """
        Informs the renderer to load a mesh,
        enables the mesh settings
        :param mesh_data: MeshData
        :return:
        """
        self._scene_renderer.load_mesh(mesh_data)
        if not self._scene_loaded:
            self._scene_loaded = True
            scene_settings = self._scene_renderer.get_scene_option_settings()
            self._view_render_options.load_scene_settings(scene_settings)
            self._view_render_options.set_scene_settings_enabled(True)

    def load_scene(self, camera_data, mesh_data):
        """
        Informs the renderer to load the 3D scene from the data,
        loading camera and mesh data. Enables scene settings.
        :param camera_data:
        :param mesh_data:
        :return:
        """
        pass

    def load_traced_paths(self, render_data):
        """
        Informs the renderer to
        :param render_data:
        :return:
        """
        self._scene_renderer.load_traced_paths(render_data)
        #self._view_render_options.set_general_settings_enabled(True)

    def display_traced_paths(self, indices):
        """
        Informs the renderer to display all path which are in the indices list
        :param indices: numpy array containing path indices
        :return:
        """
        self._scene_renderer.display_traced_paths(indices)

    def clear_traced_paths(self):
        """
        Informs the renderer to clear all visualizes traced paths
        :return:
        """
        self._renderer.clear_paths()

    def send_update_path(self, indices, add_item):
        """
        Informs the controller to visualize or add the path depending on add_item value
        :param indices: numpy array containing path indices
        :param add_item: boolean
        :return:
        """
        self._controller.update_path(indices, add_item)

    def select_path(self, index):
        """
        Informs the renderer to visualize the path with index: index
        :param index: integer
        :return:
        """
        self._scene_renderer.select_path(index)
        #self._view_render_options.load_path_settings()
        #self._view_render_options.set_path_settings_enabled(True)

    def select_vertex(self, tpl):
        """
        Informs the renderer to select / highlight the vertex with tuple tpl
        :param tpl: tuple(path_index, vertex_index)
        :return:
        """
        self._scene_renderer.select_vertex(tpl)
        #self._view_render_options.load_vertex_settings()
        #self._view_render_options.set_vertex_settings_enabled(True)

    def send_select_path(self, index):
        """
        Informs the controller to select the path with index: index
        :param index: integer
        :return:
        """
        self._controller.select_path(index)

    def send_select_vertex(self, tpl):
        """
        Informs the controller to select the vertex with tuple tpl
        :param tpl: tuple(path_index, vertex_index)
        :return:
        """
        self._controller.select_vertex(tpl)

    def close(self):
        """
        Closes the view render scene options
        :return:
        """
        self._view_render_options.close()
