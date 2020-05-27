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

from Core.pyside2_uic import loadUi
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QApplication
import logging


class SceneRenderSettings(object):

    def __init__(self, view):
        self._init(view)

    def update(self, view):
        self._init(view)

    def _init(self, view):
        # Save general Scene options settings
        self.is_all_nees_visible = view.cbShowAllNEEs.isChecked()
        self.is_all_paths_visible = view.cbShowAllPaths.isChecked()
        self.is_all_verts_visible = view.cbShowAllVerts.isChecked()

        # Save path options settings
        self.is_path_visible = view.cbShowPathRays.isChecked()
        self.is_path_ne_visible = view.cbShowNEERays.isChecked()
        self.path_opacity = view.sliderPathOpacity.value()
        self.path_size = view.sliderPathSize.value()
        self.is_show_all_other_paths = view.cbShowAllOtherPaths.isChecked()

        # Save vertex option settings
        self.is_omega_i_visible = view.cbShowOmegaI.isChecked()
        self.is_omega_o_visible = view.cbShowOmegaO.isChecked()
        self.is_vertex_ne_visible = view.cbShowNEE.isChecked()
        self.vert_opacity = view.sliderVertexOpacity.value()
        self.vert_size = view.sliderVertexSize.value()
        self.is_show_all_other_verts = view.cbShowAllOtherVertices.isChecked()


class ViewRenderSceneOptions(QWidget):

    """
        ViewRenderSceneOptions
        Handles the view render scene options view and all user inputs.
        Informs the render interface about view changes
    """

    def __init__(self):
        QWidget.__init__(self, parent=None)
        loadUi('View/ui/render_scene_options.ui', self)

        self._renderer = None

        # center widget depending on screen size
        desktop_widget = QApplication.desktop()
        screen_rect = desktop_widget.availableGeometry(self)
        self.move(screen_rect.center() - self.rect().center())

        # handle close btn
        self.btnQuit.clicked.connect(self.close)

        # handle general settings
        self.cbShowAllNEEs.toggled.connect(self.show_all_nees)
        self.cbShowAllPaths.toggled.connect(self.show_all_paths)
        self.cbShowAllVerts.toggled.connect(self.show_all_verts)

        # handle camera settings
        self.sliderCameraSpeed.valueChanged.connect(self.update_camera_motion_speed)
        self.cbCameraClipping.toggled.connect(self.update_camera_clipping)
        self.pbResetCamera.clicked.connect(self.reset_camera_options)

        # handle scene settings
        self.sliderMeshOpacity.valueChanged.connect(self.update_scene_opacity)
        self.pbResetMesh.clicked.connect(self.reset_scene_opacity)

        # handle path settings
        self.sliderPathOpacity.valueChanged.connect(self.update_path_opacity)
        self.sliderPathSize.valueChanged.connect(self.update_path_size)
        self.pbResetPath.clicked.connect(self.reset_path)
        self.cbShowPathRays.toggled.connect(self.show_traced_path)
        self.cbShowNEERays.toggled.connect(self.show_traced_path_nee)
        self.cbShowAllOtherPaths.toggled.connect(self.show_other_paths)

        # handle vertex settings
        self.sliderVertexOpacity.valueChanged.connect(self.update_vertex_opacity)
        self.sliderVertexSize.valueChanged.connect(self.update_vertex_size)
        self.pbResetVertex.clicked.connect(self.reset_vertex)
        self.cbShowOmegaI.toggled.connect(self.show_vertex_omega_i)
        self.cbShowOmegaO.toggled.connect(self.show_vertex_omega_o)
        self.cbShowNEE.toggled.connect(self.show_vertex_nee)
        self.cbShowAllOtherVertices.toggled.connect(self.show_other_verts)

        self._settings = SceneRenderSettings(self)

    def set_renderer(self, renderer):
        self._renderer = renderer

    def prepare_new_data(self):
        """
        Prepare view for new incoming render data,
        disables path and vertex settings
        :return:
        """
        self.set_path_settings_enabled(False)
        self.set_vertex_settings_enabled(False)
        self.save_current_settings()

    def save_current_settings(self):
        """
        Saves current scene option settings
        :return:
        """
        self._settings.update(self)

    def set_general_settings_enabled(self, enabled):
        """
        Depending on enabled, enables the general render scene settings
        :param enabled: boolean
        :return:
        """
        self.widgetBtnsGeneral.setEnabled(enabled)

    def set_camera_settings_enabled(self, enabled):
        """
        Depending on enabled, enables the camera settings
        :param enabled:
        :return:
        """
        self.widgetCamera.setEnabled(enabled)
        self.widgetBtnsCamera.setEnabled(enabled)

    def load_camera_settings(self):
        """
        Initialises the camera settings with data from the renderer
        :return:
        """
        motion_speed = self._renderer.get_camera_motion_speed()
        self.sliderCameraSpeed.blockSignals(True)
        self.sliderCameraSpeed.setValue(motion_speed)
        self.sliderCameraSpeed.blockSignals(False)
        camera_clipping = self._renderer.camera_clipping()
        self.cbCameraClipping.blockSignals(True)
        self.cbCameraClipping.setChecked(camera_clipping)
        self.cbCameraClipping.blockSignals(False)

    def set_scene_settings_enabled(self, enabled):
        """
        Depending on enabled, enables the scene settings
        :param enabled: boolean
        :return:
        """
        self.widgetMesh.setEnabled(enabled)
        self.widgetBtnsMesh.setEnabled(enabled)

    def load_scene_settings(self):
        """
        Initializes the scene settings with data from the renderer
        :return:
        """
        opacity = self._renderer.get_scene_opacity()
        max_value = self.sliderMeshOpacity.maximum()
        self.sliderMeshOpacity.blockSignals(True)
        self.sliderMeshOpacity.setValue(int(opacity * max_value))
        self.sliderMeshOpacity.blockSignals(False)

    def set_path_settings_enabled(self, enabled):
        """
        Depending on enabled, enables the path settings
        :param enabled: boolean
        :return:
        """
        self.widgetPath.setEnabled(enabled)
        self.widgetBtnsPath.setEnabled(enabled)

    def load_path_settings(self):
        """
        Loads the path settings loaded from the renderer
        :return:
        """
        index = self._renderer.get_selected_path_index()
        self.labelPathIndex.setText("({})".format(index))
        opacity = self._renderer.get_path_opacity(index)
        max_value = self.sliderPathOpacity.maximum()
        self.sliderPathOpacity.blockSignals(True)
        self.sliderPathOpacity.setValue(int(opacity * max_value))
        self.sliderPathOpacity.blockSignals(False)
        size = self._renderer.get_path_size(index)
        self.sliderPathSize.blockSignals(True)
        self.sliderPathSize.setValue(size)
        self.sliderPathSize.blockSignals(False)
        show_path = self._renderer.get_is_visible_path(index)
        self.cbShowPathRays.blockSignals(True)
        self.cbShowPathRays.setChecked(show_path)
        self.cbShowPathRays.blockSignals(False)
        show_path_ne = self._renderer.get_is_ne_visible_path(index)
        self.cbShowNEERays.blockSignals(True)
        self.cbShowNEERays.setChecked(show_path_ne)
        self.cbShowNEERays.blockSignals(False)

    def set_vertex_settings_enabled(self, enabled):
        """
        Depending on enabled, enables the vertex settings
        :param enabled:
        :return: boolean
        """
        self.widgetVertex.setEnabled(enabled)
        self.widgetBtnsVertex.setEnabled(enabled)

    def load_vertex_settings(self):
        """
        Loads the vertex settings loaded from the renderer
        :return:
        """
        tpl = self._renderer.get_selected_vertex_tpl()
        self.labelVertexIndex.setText("{}".format(tpl))
        is_wi_visible = self._renderer.is_wi_visible(tpl)
        self.cbShowOmegaI.blockSignals(True)
        self.cbShowOmegaI.setChecked(is_wi_visible)
        self.cbShowOmegaI.blockSignals(False)
        is_wo_visible = self._renderer.is_wo_visible(tpl)
        self.cbShowOmegaO.blockSignals(True)
        self.cbShowOmegaO.setChecked(is_wo_visible)
        self.cbShowOmegaO.blockSignals(False)
        is_ne_visible = self._renderer.is_ne_visible(tpl)
        self.cbShowNEE.blockSignals(True)
        self.cbShowNEE.setChecked(is_ne_visible)
        self.cbShowNEE.blockSignals(False)
        opacity = self._renderer.get_vertex_opacity(tpl)
        max_value = self.sliderVertexOpacity.maximum()
        self.sliderVertexOpacity.blockSignals(True)
        self.sliderVertexOpacity.setValue(int(opacity * max_value))
        self.sliderVertexOpacity.blockSignals(False)
        size = self._renderer.get_vertex_size(tpl)
        self.sliderVertexSize.blockSignals(True)
        self.sliderVertexSize.setValue(size)
        self.sliderVertexSize.blockSignals(False)

    @Slot(bool, name='show_all_nees')
    def show_all_nees(self, state):
        """
        Informs the renderer to show all next event estimations
        :param state:
        :return:
        """
        self.cbShowNEERays.blockSignals(True)
        self.cbShowNEERays.setChecked(state)
        self.cbShowNEERays.blockSignals(False)
        self._renderer.show_all_nees(state)

    @Slot(bool, name='show_all_paths')
    def show_all_paths(self, state):
        """
        Informs the renderer to show all traced paths
        :param state:
        :return:
        """
        if state:
            self.cbShowPathRays.blockSignals(True)
            self.cbShowPathRays.setChecked(state)
            self.cbShowPathRays.blockSignals(False)
        self._renderer.show_all_paths(state)

    @Slot(bool, name='show_all_verts')
    def show_all_verts(self, state):
        """
        Informs the renderer to show all vertices
        :param state:
        :return:
        """
        self._renderer.show_all_verts(state)

    @Slot(int, name='update_camera_motion_speed')
    def update_camera_motion_speed(self, speed):
        """
        Informs the renderer to update the camera motion speed
        :param speed: float
        :return:
        """
        self._renderer.update_camera_motion_speed(speed)

    @Slot(bool, name='update_camera_clipping')
    def update_camera_clipping(self, state):
        """
        Informs the renderer to update camera clipping
        :param state: boolean
        :return:
        """
        self._renderer.update_camera_clipping(state)

    @Slot(bool, name='reset_camera_options')
    def reset_camera_options(self, clicked):
        """
        Inform the renderer to reset the camera settings
        :param clicked: boolean
        :return:
        """
        self._renderer.reset_camera_motion_speed()
        self.load_camera_settings()

    @Slot(int, name='update_scene_opacity')
    def update_scene_opacity(self, opacity):
        """
        Informs the renderer to update the scene opacity
        :param opacity: float[0,1]
        :return:
        """
        max_value = self.sliderMeshOpacity.maximum()
        self._renderer.update_scene_opacity(float(opacity / max_value))

    @Slot(bool, name='reset_scene_opacity')
    def reset_scene_opacity(self, clicked):
        """
        Informs the renderer to reset the scenes opacity
        :param clicked: boolean
        :return:
        """
        self._renderer.reset_scene_opacity()
        self.load_scene_settings()

    @Slot(int, name='update_path_opacity')
    def update_path_opacity(self, opacity):
        """
        Informs the renderer to update the path opacity
        :param opacity: float[0,1]
        :return:
        """
        max_value = self.sliderPathOpacity.maximum()
        self._renderer.update_path_opacity(float(opacity / max_value))

    @Slot(int, name='update_path_size')
    def update_path_size(self, size):
        """
        Informs the renderer to update the path size
        :param size: float[0,1]
        :return:
        """
        self._renderer.update_path_size(size)

    @Slot(bool, name='reset_path')
    def reset_path(self, clicked):
        """
        Informs the renderer to reset the paths size and opacity
        :param clicked: boolean
        :return:
        """
        self._renderer.reset_path()
        self.load_path_settings()

    @Slot(bool, name='show_traced_path')
    def show_traced_path(self, state):
        """
        Informs the renderer to show all traced paths
        :param state: boolean
        :return:
        """
        self._renderer.show_traced_path(state)
        # toggle also vertex omega_i checkbox
        self.cbShowOmegaI.blockSignals(True)
        self.cbShowOmegaI.setChecked(state)
        self.cbShowOmegaI.blockSignals(False)

    @Slot(bool, name='show_traced_path_nee')
    def show_traced_path_nee(self, state):
        """
        Informs the renderer to show paths next event estimations
        :param state: boolean
        :return:
        """
        self._renderer.show_traced_path_nee(state)
        # toggle also vertex nee checkbox
        self.cbShowNEE.blockSignals(True)
        self.cbShowNEE.setChecked(state)
        self.cbShowNEE.blockSignals(False)

    @Slot(bool, name='show_other_paths')
    def show_other_paths(self, state):
        """
        Informs the renderer to show all other traced paths besides the current selected one
        :param state: boolean
        :return:
        """
        self._renderer.show_other_paths(state)

    @Slot(int, name='update_vertex_opacity')
    def update_vertex_opacity(self, opacity):
        """
        Informs the renderer to update the vertex opacity of the current selected vertex
        :param opacity: float[0,1]
        :return:
        """
        max_value = self.sliderVertexOpacity.maximum()
        self._renderer.update_vertex_opacity(float(opacity / max_value))

    @Slot(int, name='update_vertex_size')
    def update_vertex_size(self, size):
        """
        Informs the renderer to update the vertex size of the current selected vertex
        :param size: float[0,1]
        :return:
        """
        self._renderer.update_vertex_size(size)

    @Slot(bool, name='reset_vertex')
    def reset_vertex(self, clicked):
        """
        Informs the renderer to reset the vertex opacity and size
        :param clicked: boolean
        :return:
        """
        self._renderer.reset_vertex()
        self.load_vertex_settings()

    @Slot(bool, name='show_vertex_omega_i')
    def show_vertex_omega_i(self, state):
        """
        Informs the renderer to visualize the incoming ray of the current selected vertex,
        depending on state
        :param state: boolean
        :return:
        """
        self._renderer.show_vertex_omega_i(state)

    @Slot(bool, name='show_vertex_omega_o')
    def show_vertex_omega_o(self, state):
        """
        Informs the renderer to visualize the outgoing ray of the current selected vertex,
        depending on state
        :param state: boolean
        :return:
        """
        self._renderer.show_vertex_omega_o(state)

    @Slot(bool, name='show_vertex_nee')
    def show_vertex_nee(self, state):
        """
        Informs the renderer to visualize the next event estimation of the current selected vertex,
        depending on state
        :param state: boolean
        :return:
        """
        self._renderer.show_vertex_nee(state)

    @Slot(bool, name='show_other_verts')
    def show_other_verts(self, state):
        """
        Informs the renderer to visualize all other vertices besides the current visible ones,
        depending on state
        :param state: boolean
        :return:
        """
        self._renderer.show_other_verts(state)
