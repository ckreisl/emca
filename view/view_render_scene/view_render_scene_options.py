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

from core.pyside2_uic import loadUi
from core.list_items import PathListItem
from core.list_items import VertexListItem
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QListWidgetItem
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QApplication
import os
import logging


class ViewRenderSceneOptions(QWidget):

    """
        ViewRenderSceneOptions
        Handles the view render scene options view and all user inputs.
        Informs the render interface about view changes
    """

    def __init__(self, parent):
        QWidget.__init__(self, parent=None)
        ui_filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ui', 'render_scene_options.ui'))
        loadUi(ui_filepath, self)

        self._controller = None

        # center widget depending on screen size
        desktop_widget = QApplication.desktop()
        screen_rect = desktop_widget.availableGeometry(self)
        self.move(screen_rect.center() - self.rect().center())

        # handle close btn
        self.pbClose.clicked.connect(self.close)

        # add connections to controller
        self.listPaths.itemClicked.connect(self.send_select_path)
        self.listVertices.itemClicked.connect(self.send_select_intersection)

    def set_controller(self, controller):
        self._controller = controller
        # handle general settings
        self.cbShowAllNEEs.toggled.connect(controller.scene.show_all_traced_nees)
        self.cbShowAllVerts.toggled.connect(controller.scene.show_all_traced_vertices)
        self.cbShowAllPaths.toggled.connect(controller.show_all_traced_paths)

        # handle camera settings
        self.sliderCameraSpeed.valueChanged.connect(controller.scene.update_camera_motion_speed)
        self.cbCameraClipping.toggled.connect(controller.scene.update_camera_clipping)
        self.pbResetCamera.clicked.connect(controller.scene.reset_camera_motion_speed)

        # handle scene settings
        self.sliderMeshOpacity.valueChanged.connect(controller.scene.update_mesh_opacity)
        self.sliderSceneOpacity.valueChanged.connect(controller.scene.update_scene_opacity)
        self.pbResetMesh.clicked.connect(controller.scene.reset_mesh)
        self.pbResetScene.clicked.connect(controller.scene.reset_scene)

        # handle path settings
        self.sliderPathOpacity.valueChanged.connect(controller.scene.update_path_opacity)
        self.sliderPathSize.valueChanged.connect(controller.scene.update_path_size)
        self.pbResetPath.clicked.connect(controller.scene.reset_path)
        self.cbShowPathRays.toggled.connect(controller.scene.show_traced_path)
        self.cbShowNEERays.toggled.connect(controller.scene.show_traced_path_nee)
        self.cbShowAllOtherPaths.toggled.connect(controller.scene.show_all_other_traced_paths)

        # handle vertex settings
        self.sliderVertexOpacity.valueChanged.connect(controller.scene.update_vertex_opacity)
        self.sliderVertexSize.valueChanged.connect(controller.scene.update_vertex_size)
        self.pbResetVertex.clicked.connect(controller.scene.reset_vertex)
        self.cbShowOmegaI.toggled.connect(controller.scene.show_vertex_omega_i)
        self.cbShowOmegaO.toggled.connect(controller.scene.show_vertex_omega_o)
        self.cbShowNEE.toggled.connect(controller.scene.show_vertex_nee)
        self.cbShowAllOtherVertices.toggled.connect(controller.scene.show_all_other_traced_vertices)

        self.pbInspectSelectedPath.clicked.connect(controller.scene.inspect_selected_path)
        self.pbResetAll.clicked.connect(controller.scene.reset_all_paths_vertices)

    @Slot(QListWidgetItem, name='send_select_path')
    def send_select_path(self, item):
        if isinstance(item, PathListItem):
            self._controller.select_path(item.path_index)

    @Slot(QListWidgetItem, name='send_select_intersection')
    def send_select_intersection(self, item):
        if isinstance(item, VertexListItem):
            self._controller.select_intersection(item.index_tpl)

    @Slot(bool, name='inspect_selected_path')
    def inspect_selected_path(self, clicked):
        self._controller.scene.inspect_selected_path(clicked)
        
    def update_path_indices(self, indices):
        self.listPaths.clear()
        self.listVertices.clear()
        for key in indices:
            self.listPaths.addItem(PathListItem(key))
        if not self.listPaths.isEnabled():
            self.listPaths.setEnabled(True)
        if not self.labelPathOptions.isEnabled():
            self.labelPathOptions.setEnabled(True)
        if not self.cbShowAllOtherPaths.isEnabled():
            self.cbShowAllOtherPaths.setEnabled(True)
        self.enable_general_settings(True)

    def select_path(self, index):
        self.enable_path_settings(True)
        self.labelVertexOptions.setEnabled(True)
        self.listVertices.setEnabled(True)
        self.cbShowAllOtherVertices.setEnabled(True)
        # highlight selected path item in list.
        for i in range(0, self.listPaths.count()):
            item = self.listPaths.item(i)
            if item.path_index == index:
                item.setSelected(True)
                break

    def select_intersection(self, tpl):
        self.enable_vertex_settings(True)
        # highlight selected vertex item in list.
        for i in range(0, self.listVertices.count()):
            item = self.listVertices.item(i)
            if item.vertex_index == tpl[1]:
                item.setSelected(True)
                break

    def update_vertex_list(self, path_data):
        self.listVertices.clear()
        for key, _ in path_data.intersections.items():
            self.listVertices.addItem(VertexListItem((path_data.sample_idx, key)))

    def prepare_new_data(self):
        """
        Prepare view for new incoming render data,
        disables path and vertex settings
        :return:
        """
        self.listPaths.clear()
        self.listVertices.clear()
        self.enable_path_settings(False)
        self.enable_vertex_settings(False)

    def enable_general_settings(self, enabled):
        """
        Depending on enabled, enables the general render scene settings
        :param enabled: boolean
        :return:
        """
        self.labelGeneral.setEnabled(enabled)
        self.cbShowAllPaths.setEnabled(enabled)
        self.cbShowAllNEEs.setEnabled(enabled)
        self.cbShowAllVerts.setEnabled(enabled)

    def enable_camera_settings(self, enabled):
        """
        Depending on enabled, enables the camera settings
        :param enabled:
        :return:
        """
        self.labelMotionSpeed.setEnabled(enabled)
        self.labelCameraClipping.setEnabled(enabled)
        self.sliderCameraSpeed.setEnabled(enabled)
        self.cbCameraClipping.setEnabled(enabled)
        self.pbResetCamera.setEnabled(enabled)

    def enable_scene_settings(self, enabled):
        """
        Depending on enabled, enables the scene settings
        :param enabled: boolean
        :return:
        """
        # TODO scene mesh list feature
        # self.listSceneObjects.setEnabled(enabled)
        # self.labelMeshOpacity.setEnabled(enabled)
        # self.sliderMeshOpacity.setEnabled(enabled)
        # self.pbMeshOpacity.setEnabled(enabled)
        # self.pbResetMesh.setEnabled(enabled)
        self.labelSceneOpacity.setEnabled(enabled)
        self.sliderSceneOpacity.setEnabled(enabled)
        self.pbResetScene.setEnabled(enabled)

    def enable_path_settings(self, enabled):
        """
        Depending on enabled, enables the path settings
        :param enabled: boolean
        :return:
        """
        self.labelPathOptions.setEnabled(enabled)
        self.listPaths.setEnabled(enabled)
        self.labelShowPath.setEnabled(enabled)
        self.cbShowPathRays.setEnabled(enabled)
        self.labelShowPathNE.setEnabled(enabled)
        self.cbShowNEERays.setEnabled(enabled)
        self.labelPathOpacity.setEnabled(enabled)
        self.sliderPathOpacity.setEnabled(enabled)
        self.labelPathSize.setEnabled(enabled)
        self.sliderPathSize.setEnabled(enabled)
        self.pbResetPath.setEnabled(enabled)
        self.cbShowAllOtherPaths.setEnabled(enabled)
        self.pbResetAll.setEnabled(enabled)
        self.pbInspectSelectedPath.setEnabled(enabled)

    def enable_vertex_settings(self, enabled):
        """
        Depending on enabled, enables the vertex settings
        :param enabled:
        :return:
        """
        self.labelVertexOptions.setEnabled(enabled)
        self.listVertices.setEnabled(enabled)
        self.labelShowOmegaI.setEnabled(enabled)
        self.cbShowOmegaI.setEnabled(enabled)
        self.labelShowOmegaO.setEnabled(enabled)
        self.cbShowOmegaO.setEnabled(enabled)
        self.labelShowNE.setEnabled(enabled)
        self.cbShowNEE.setEnabled(enabled)
        self.labelVertexOpacity.setEnabled(enabled)
        self.sliderVertexOpacity.setEnabled(enabled)
        self.labelVertexSize.setEnabled(enabled)
        self.sliderVertexSize.setEnabled(enabled)
        self.cbShowAllOtherVertices.setEnabled(enabled)
        self.pbResetVertex.setEnabled(enabled)

    def load_camera_settings(self, camera_settings):
        """
        Initialises the camera settings with data from the renderer
        :param camera_settings: dict
        :return:
        """
        self.sliderCameraSpeed.blockSignals(True)
        self.sliderCameraSpeed.setValue(camera_settings.get('motion_speed', 1.0))
        self.sliderCameraSpeed.blockSignals(False)
        self.cbCameraClipping.blockSignals(True)
        self.cbCameraClipping.setChecked(camera_settings.get('auto_clipping', True))
        self.cbCameraClipping.blockSignals(False)

    def load_scene_settings(self, scene_settings):
        """
        Initializes the scene settings with data from the renderer
        :param scene_settings: dict
        :return:
        """
        opacity = scene_settings.get('scene_opacity', 1.0)
        max_value = self.sliderMeshOpacity.maximum()
        self.sliderMeshOpacity.blockSignals(True)
        self.sliderMeshOpacity.setValue(int(opacity * max_value))
        self.sliderMeshOpacity.blockSignals(False)
        max_value = self.sliderSceneOpacity.maximum()
        self.sliderSceneOpacity.blockSignals(True)
        self.sliderSceneOpacity.setValue(int(opacity * max_value))
        self.sliderSceneOpacity.blockSignals(False)

    def load_path_settings(self, path_option_settings):
        """
        Loads the path settings loaded from the renderer
        :param path_option_settings: dict
        :return:
        """
        opacity = path_option_settings.get('opacity', 1.0)
        max_value = self.sliderPathOpacity.maximum()
        self.sliderPathOpacity.blockSignals(True)
        self.sliderPathOpacity.setValue(int(opacity * max_value))
        self.sliderPathOpacity.blockSignals(False)

        size = path_option_settings.get('size', 1.0)
        self.sliderPathSize.blockSignals(True)
        self.sliderPathSize.setValue(size)
        self.sliderPathSize.blockSignals(False)

        show_path = path_option_settings.get('is_visible', True)
        self.cbShowPathRays.blockSignals(True)
        self.cbShowPathRays.setChecked(show_path)
        self.cbShowPathRays.blockSignals(False)

        show_path_ne = path_option_settings.get('is_ne_visible', False)
        self.cbShowNEERays.blockSignals(True)
        self.cbShowNEERays.setChecked(show_path_ne)
        self.cbShowNEERays.blockSignals(False)

    def load_vertex_settings(self, vertex_option_settings):
        """
        Loads the vertex settings loaded from the renderer
        :param vertex_option_settings: dict
        :return:
        """
        is_wi_visible = vertex_option_settings.get('is_wi_visible', True)
        self.cbShowOmegaI.blockSignals(True)
        self.cbShowOmegaI.setChecked(is_wi_visible)
        self.cbShowOmegaI.blockSignals(False)

        is_wo_visible = vertex_option_settings.get('is_wo_visible', False)
        self.cbShowOmegaO.blockSignals(True)
        self.cbShowOmegaO.setChecked(is_wo_visible)
        self.cbShowOmegaO.blockSignals(False)

        is_ne_visible = vertex_option_settings.get('is_ne_visible', False)
        self.cbShowNEE.blockSignals(True)
        self.cbShowNEE.setChecked(is_ne_visible)
        self.cbShowNEE.blockSignals(False)

        opacity = vertex_option_settings.get('opacity', 1.0)
        max_value = self.sliderVertexOpacity.maximum()
        self.sliderVertexOpacity.blockSignals(True)
        self.sliderVertexOpacity.setValue(int(opacity * max_value))
        self.sliderVertexOpacity.blockSignals(False)

        size = vertex_option_settings.get('size', 1.0)
        self.sliderVertexSize.blockSignals(True)
        self.sliderVertexSize.setValue(size)
        self.sliderVertexSize.blockSignals(False)
