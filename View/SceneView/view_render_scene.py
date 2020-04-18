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
from Renderer.renderer import Renderer
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import uic
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
        uic.loadUi(ui_filepath, self)

        self._controller = None

        # init renderer
        self._renderer = Renderer()

        # init scene options with renderer
        self._view_render_options = ViewRenderSceneOptions()
        self._view_render_options.set_renderer(self._renderer)

        # connect renderer to views
        self._renderer.set_view_render_scene(self)
        self._renderer.set_view_render_scene_options(self._view_render_options)

        # add render widget to view
        self.sceneLayout.addWidget(self._renderer.widget)

        self.btnSceneOptions.clicked.connect(self.open_view_render_options)
        self.btnLoadScene.clicked.connect(self.request_scene)
        self.btnReset.clicked.connect(self.reset)
        # Currently buggy, returns sometimes a black image of the scene view.
        #self.btnScreenshot.clicked.connect(self.screenshot)
        self.btnScreenshot.deleteLater()

    def set_renderer(self, renderer):
        self._renderer = renderer

    def set_controller(self, controller):
        """
        Sets the connection to the controller
        :param controller: Controller
        :return:
        """
        self._controller = controller

    @pyqtSlot(bool, name='open_view_render_options')
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

    @pyqtSlot(bool, name='load_scene')
    def request_scene(self, clicked):
        """
        Informs the controller to request the 3D scene data from the server
        :param clicked: boolean
        :return:
        """
        self._renderer.clear_scene_objects()
        self._controller.request_scene_data()

    @pyqtSlot(bool, name='reset')
    def reset(self, clicked):
        """
        Informs the renderer to reset the scenes camera view
        :param clicked: boolean
        :return:
        """
        self._renderer.reset_scene()

    @pyqtSlot(bool, name='screenshot')
    def screenshot(self, clicked):
        """
        Informs the renderer to take a screenshot of the view and save it under the given filename
        :param clicked: boolean
        :return:
        """
        dialog = QFileDialog(self)
        dialog.setNameFilter("Images (*.png *.jpg)")
        dialog.selectNameFilter("Images (*.png *.jpg)")
        filename = dialog.getSaveFileName(self)[0]
        if filename:
            self._renderer.take_screenshot(filename)

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
            # TODO disabled because of buggy behaviour
            #self.btnScreenshot.setEnabled(enabled)
        elif mode is ViewMode.XML:
            self.btnReset.setEnabled(enabled)
            self.btnSceneOptions.setEnabled(enabled)
            # comment out because of buggy behaviour when taking a screenshot
            # self.btnScreenshot.setEnabled(enabled)

    def prepare_new_data(self):
        """
        Prepare new incoming data, informs the renderer that new data is coming
        :return:
        """
        self._view_render_options.prepare_new_data()
        self._renderer.prepare_new_data()

    def remove_scene_objects(self):
        """
        Informs the renderer to clear all objects within the scene
        :return:
        """
        self._renderer.clear_scene_objects()

    def load_camera(self, camera_data):
        """
        Informs the renderer about the camera data,
        loads the camera data and enables the camera settings
        :param camera_data:
        :return:
        """
        self._renderer.load_camera(camera_data)
        self._view_render_options.load_camera_settings()
        self._view_render_options.set_camera_settings_enabled(True)

    def load_mesh(self, mesh_data):
        """
        Informs the renderer to load a mesh,
        enables the mesh settings
        :param mesh_data: MeshData
        :return:
        """
        self._renderer.load_mesh(mesh_data)
        # todo is called #mesh times just enable settings once
        self._view_render_options.load_scene_settings()
        self._view_render_options.set_scene_settings_enabled(True)

    def load_scene(self, camera_data, mesh_data):
        """
        Informs the renderer to load the 3D scene from the data,
        loading camera and mesh data. Enables scene settings.
        :param camera_data:
        :param mesh_data:
        :return:
        """
        self._renderer.load_scene(camera_data, mesh_data)
        self._view_render_options.load_camera_settings()
        self._view_render_options.load_scene_settings()
        self._view_render_options.set_camera_settings_enabled(True)
        self._view_render_options.set_scene_settings_enabled(True)

    def load_traced_paths(self, render_data):
        """
        Informs the renderer to
        :param render_data:
        :return:
        """
        self._renderer.load_traced_paths(render_data)
        self._view_render_options.set_general_settings_enabled(True)

    def display_traced_paths(self, indices):
        """
        Informs the renderer to display all path which are in the indices list
        :param indices: numpy array containing path indices
        :return:
        """
        self._renderer.display_traced_paths(indices)

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
        self._renderer.select_path(index)
        self._view_render_options.load_path_settings()
        self._view_render_options.set_path_settings_enabled(True)

    def select_vertex(self, tpl):
        """
        Informs the renderer to select / highlight the vertex with tuple tpl
        :param tpl: tuple(path_index, vertex_index)
        :return:
        """
        self._renderer.select_vertex(tpl)
        self._view_render_options.load_vertex_settings()
        self._view_render_options.set_vertex_settings_enabled(True)

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
