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
from PySide2.QtWidgets import QListWidgetItem
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QApplication
import logging


class PathListItem(QListWidgetItem):

    def __init__(self, path_index):
        super().__init__()
        self._path_index = path_index
        self.setText("Path ({})".format(path_index))

    @property
    def path_index(self):
        return self._path_index


class VertexListItem(QListWidgetItem):

    def __init__(self, tpl):
        super().__init__()
        self._tpl = tpl
        self.setText("Vertex ({})".format(tpl[1]))

    @property
    def path_index(self):
        """
        Returns the index of the parent, representing the path index
        :return: integer
        """
        return self._tpl[0]

    @property
    def vertex_index(self):
        """
        Returns the vertex index
        :return: integer
        """
        return self._tpl[1]

    @property
    def index_tpl(self):
        """
        Returns a tuple containing path and vertex index
        :return: tuple(path_index, vertex_index)
        """
        return self._tpl


class ViewRenderSceneOptions(QWidget):

    """
        ViewRenderSceneOptions
        Handles the view render scene options view and all user inputs.
        Informs the render interface about view changes
    """

    def __init__(self):
        QWidget.__init__(self, parent=None)
        loadUi('View/ui/render_scene_options.ui', self)

        self._controller = None
        self._scene_renderer = None

        # center widget depending on screen size
        desktop_widget = QApplication.desktop()
        screen_rect = desktop_widget.availableGeometry(self)
        self.move(screen_rect.center() - self.rect().center())

        # handle close btn
        self.pbClose.clicked.connect(self.close)

        # handle general settings
        self.cbShowAllNEEs.toggled.connect(self.show_all_nees)
        self.cbShowAllPaths.toggled.connect(self.show_all_paths)
        self.cbShowAllVerts.toggled.connect(self.show_all_verts)

        # handle camera settings
        self.sliderCameraSpeed.valueChanged.connect(self.update_camera_motion_speed)
        self.cbCameraClipping.toggled.connect(self.update_camera_clipping)
        self.pbResetCamera.clicked.connect(self.reset_camera_motion_speed)

        # handle scene settings
        self.sliderMeshOpacity.valueChanged.connect(self.update_mesh_opacity)
        self.sliderSceneOpacity.valueChanged.connect(self.update_scene_opacity)
        self.pbResetMesh.clicked.connect(self.reset_mesh)
        self.pbResetScene.clicked.connect(self.reset_scene)

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

        # add connections to controller
        self.listPaths.itemClicked.connect(self.send_select_path)
        self.listVertices.itemClicked.connect(self.send_select_vertex)

    def set_controller(self, controller):
        self._controller = controller

    def init_scene_renderer(self, scene_renderer):
        self._scene_renderer = scene_renderer

    @Slot(QListWidgetItem, name='send_select_path')
    def send_select_path(self, item):
        if isinstance(item, PathListItem):
            self._controller.select_path(item.path_index)

    @Slot(QListWidgetItem, name='send_select_vertex')
    def send_select_vertex(self, item):
        if isinstance(item, VertexListItem):
            self._controller.select_vertex(item.index_tpl)

    def update_path_indices(self, indices):
        self.listPaths.clear()
        self.listVertices.clear()
        for key in indices:
            self.listPaths.addItem(PathListItem(key))
        self.listPaths.setEnabled(True)
        self.labelPathOptions.setEnabled(True)
        self.cbShowAllOtherPaths.setEnabled(True)
        self.enable_general_settings(True)

    def select_path(self, index):
        path_option_settings = self._scene_renderer.get_path_option_settings(index)
        self.load_path_settings(path_option_settings)
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

    def select_vertex(self, tpl):
        vertex_option_settings = self._scene_renderer.get_vertex_option_settings(tpl)
        self.load_vertex_settings(vertex_option_settings)
        self.enable_vertex_settings(True)
        # highlight selected vertex item in list.
        for i in range(0, self.listVertices.count()):
            item = self.listVertices.item(i)
            if item.vertex_index == tpl[1]:
                item.setSelected(True)
                break

    def update_vertex_list(self, path_data):
        self.listVertices.clear()
        for key, _ in path_data.dict_vertices.items():
            self.listVertices.addItem(VertexListItem((path_data.sample_idx, key)))

    def prepare_new_data(self):
        """
        Prepare view for new incoming render data,
        disables path and vertex settings
        :return:
        """
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

    def enable_vertex_settings(self, enabled):
        """
        Depending on enabled, enables the vertex settings
        :param enabled:
        :return: boolean
        """
        self.labelVertexOptions.setEnabled(enabled)
        self.listVertices.setEnabled(enabled)
        self.labelShowOmegaI.setEnabled(enabled)
        self.labelShowOmegaO.setEnabled(enabled)
        self.labelShowNE.setEnabled(enabled)
        self.labelVertexOpacity.setEnabled(enabled)
        self.sliderVertexOpacity.setEnabled(enabled)
        self.labelVertexSize.setEnabled(enabled)
        self.sliderVertexSize.setEnabled(enabled)
        self.cbShowAllOtherVertices.setEnabled(enabled)
        self.pbResetVertex.setEnabled(enabled)

    def load_camera_settings(self, camera_settings):
        """
        Initialises the camera settings with data from the renderer
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
        self._scene_renderer.apply_path_option_settings({'all_nees_visible': state})

    @Slot(bool, name='show_all_paths')
    def show_all_paths(self, state):
        """
        Informs the renderer to show all traced paths
        :param state:
        :return:
        """
        self._scene_renderer.apply_path_option_settings({'all_paths_visible': state})

    @Slot(bool, name='show_all_verts')
    def show_all_verts(self, state):
        """
        Informs the renderer to show all vertices
        :param state:
        :return:
        """
        self._scene_renderer.apply_vertex_option_settings({'all_vertices_visible': state})

    @Slot(int, name='update_camera_motion_speed')
    def update_camera_motion_speed(self, speed):
        """
        Informs the renderer to update the camera motion speed
        :param speed: float
        :return:
        """
        self._scene_renderer.apply_camera_option_settings({'motion_speed': speed})

    @Slot(bool, name='update_camera_clipping')
    def update_camera_clipping(self, state):
        """
        Informs the renderer to update camera clipping
        :param state: boolean
        :return:
        """
        self._scene_renderer.apply_camera_option_settings({'auto_clipping': state})

    @Slot(bool, name='reset_camera_motion_speed')
    def reset_camera_motion_speed(self, clicked):
        """
        Inform the renderer to reset the camera settings
        :param clicked: boolean
        :return:
        """
        self._scene_renderer.reset_camera_option_settings()
        camera_settings = self._scene_renderer.get_camera_option_settings()
        self.load_camera_settings(camera_settings)

    @Slot(int, name='updateMeshOpacity')
    def update_mesh_opacity(self, opacity):
        pass

    @Slot(int, name='update_scene_opacity')
    def update_scene_opacity(self, opacity):
        """
        Informs the renderer to update the scene opacity
        :param opacity: float[0,1]
        :return:
        """
        max_value = self.sliderMeshOpacity.maximum()
        self._scene_renderer.apply_scene_option_settings({'scene_opacity': float(opacity / max_value)})

    @Slot(bool, name='reset_mesh')
    def reset_mesh(self, clicked):
        pass

    @Slot(bool, name='reset_scene')
    def reset_scene(self, clicked):
        """
        Informs the renderer to reset the scenes opacity
        :param clicked: boolean
        :return:
        """
        self._scene_renderer.reset_scene_option_settings()
        scene_settings = self._scene_renderer.get_scene_option_settings()
        self.load_scene_settings(scene_settings)

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
