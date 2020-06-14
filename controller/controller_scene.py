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

from PySide2.QtCore import Slot
from core.messages import StateMsg
import numpy as np


class ControllerRenderScene(object):

    """
        ControllerRenderScene
        Handles the interaction and logic with the RenderScene and RenderSceneOptions View.
    """

    def __init__(self, parent, model, view):
        self._controller_main = parent
        self._model = model
        self._view = view

    def init_scene_renderer(self, scene_renderer):
        scene_renderer.set_view_render_scene(self._view.view_render_scene)
        scene_renderer.set_view_render_scene_options(self._view.view_render_scene_options)
        self._view.view_render_scene.init_scene_renderer(scene_renderer)

    def handle_state_msg(self, tpl):
        """
        Handle current state, messages mostly received from thread,
        which listens on the socket pipeline for incoming messages
        :param tpl: (StateMsg, None or Datatype)
        :return:
        """
        msg = tpl[0]
        if msg is StateMsg.DATA_INFO:
            # automatically request scene data once render info is available
            if self._model.options_data.get_option_auto_scene_load():
                self._view.view_render_scene.clear_scene_objects()
                self._controller_main.stream.request_scene_data()
        elif msg is StateMsg.DATA_CAMERA:
            # TODO remove separate DATA_CAMERA and DATA_MESH information
            # handle both together and inform controller when everything is loaded ?!
            # thing about pros and cons
            self._view.view_render_scene.load_camera(tpl[1])
            camera_settings = self._view.view_render_scene.scene_renderer.get_camera_option_settings()
            self._view.view_render_scene_options.load_camera_settings(camera_settings)
            self._view.view_render_scene_options.enable_camera_settings(True)
        elif msg is StateMsg.DATA_MESH:
            # TODO check comment above
            self._view.view_render_scene.load_mesh(tpl[1])
            if not self._view.view_render_scene.scene_loaded:
                self._view.view_render_scene.scene_loaded = True
                scene_settings = self._view.view_render_scene.scene_renderer.get_scene_option_settings()
                self._view.view_render_scene_options.load_scene_settings(scene_settings)
                self._view.view_render_scene_options.enable_scene_settings(True)

    def reset_camera_position(self, clicked):
        """
        Reset the camera position to its default origin position
        :param clicked: boolean
        :return:
        """
        self._view.view_render_scene.scene_renderer.reset_camera_position()

    @Slot(int, name='update_camera_motion_speed')
    def update_camera_motion_speed(self, speed):
        """
        Informs the renderer to update the camera motion speed
        :param speed: float
        :return:
        """
        self._view.view_render_scene.scene_renderer.apply_camera_option_settings({'motion_speed': speed})

    @Slot(bool, name='update_camera_clipping')
    def update_camera_clipping(self, enabled):
        """
        Informs the renderer to update camera clipping
        :param enabled: boolean
        :return:
        """
        self._view.view_render_scene.scene_renderer.apply_camera_option_settings({'auto_clipping': enabled})

    @Slot(bool, name='reset_camera_motion_speed')
    def reset_camera_motion_speed(self, clicked):
        """
        Inform the renderer to reset the camera settings
        :param clicked: boolean
        :return:
        """
        scene_renderer = self._view.view_render_scene.scene_renderer
        scene_renderer.reset_camera_option_settings()
        camera_settings = scene_renderer.get_camera_option_settings()
        self._view.view_render_scene_options.load_camera_settings(camera_settings)

    @Slot(int, name='update_scene_opacity')
    def update_scene_opacity(self, opacity):
        """
        Informs the renderer to update the scene opacity
        :param opacity: float[0,1]
        :return:
        """
        max_value = self._view.view_render_scene_options.sliderMeshOpacity.maximum()
        self._view.view_render_scene.scene_renderer.apply_scene_option_settings({'scene_opacity': float(opacity / max_value)})

    @Slot(bool, name='reset_scene')
    def reset_scene(self, clicked):
        """
        Informs the renderer to reset the scenes opacity
        :param clicked: boolean
        :return:
        """
        scene_renderer = self._view.view_render_scene.scene_renderer
        scene_renderer.reset_scene_option_settings()
        scene_settings = scene_renderer.get_scene_option_settings()
        self._view.view_render_scene_options.load_scene_settings(scene_settings)

    @Slot(int, name='update_mesh_opacity')
    def update_mesh_opacity(self, opacity):
        """
        Informs the renderer about opacity update of the current selected mesh object
        :param opacity: float
        :return:
        """
        # todo
        pass

    @Slot(bool, name='reset_mesh')
    def reset_mesh(self, clicked):
        # todo
        """
        Informs the renderer to reset the current selected mesh object
        :param clicked: boolean
        """
        pass

    def inspect_selected_path(self, clicked):
        index = np.array([self._model.current_path_index])
        self._controller_main.update_path(index, False)

    @Slot(bool, name='show_traced_path')
    def show_traced_path(self, enabled):
        """
        Informs the renderer to show all traced paths
        :param enabled: boolean
        :return:
        """
        # toggle also vertex omega_i checkbox
        self._view.view_render_scene_options.cbShowOmegaI.blockSignals(True)
        self._view.view_render_scene_options.cbShowOmegaI.setChecked(enabled)
        self._view.view_render_scene_options.cbShowOmegaI.blockSignals(False)
        path_index = self._model.current_path_index
        self._view.view_render_scene.scene_renderer.show_traced_path(path_index, enabled)

    @Slot(bool, name='show_all_traced_vertices')
    def show_all_traced_vertices(self, enabled):
        """
        Informs the renderer to show all vertices
        :param enabled:
        :return:
        """
        self._view.view_render_scene.scene_renderer.show_all_traced_vertices(enabled)

    @Slot(bool, name='show_all_other_traced_vertices')
    def show_all_other_traced_vertices(self, enabled):
        """
        Informs the renderer to visualize all other vertices besides the current visible ones,
        depending on state
        :param enabled: boolean
        :return:
        """
        self._view.view_render_scene.scene_renderer.show_all_other_traced_vertices(enabled)

    @Slot(bool, name='show_all_traced_nees')
    def show_all_traced_nees(self, enabled):
        """
        Informs the renderer to show all next event estimations
        :param enabled:
        :return:
        """
        # NE checkbox path
        self._view.view_render_scene_options.cbShowNEERays.blockSignals(True)
        self._view.view_render_scene_options.cbShowNEERays.setChecked(enabled)
        self._view.view_render_scene_options.cbShowNEERays.blockSignals(False)
        # NE checkbox vertex / intersection
        self._view.view_render_scene_options.cbShowNEE.blockSignals(True)
        self._view.view_render_scene_options.cbShowNEE.setChecked(enabled)
        self._view.view_render_scene_options.cbShowNEE.blockSignals(False)
        self._view.view_render_scene.scene_renderer.show_all_traced_nees(enabled)

    @Slot(bool, name='show_all_other_traced_paths')
    def show_all_other_traced_paths(self, enabled):
        """
        Informs the renderer to show all other traced paths besides the current selected one
        :param enabled: enabled
        :return:
        """
        self._view.view_render_scene.scene_renderer.show_all_other_traced_paths(enabled)

    @Slot(bool, name='show_traced_path_nee')
    def show_traced_path_nee(self, enabled):
        """
        Informs the renderer to show paths next event estimations
        :param enabled: boolean
        :return:
        """
        # toggle also vertex nee checkbox
        self._view.view_render_scene_options.cbShowNEE.blockSignals(True)
        self._view.view_render_scene_options.cbShowNEE.setChecked(enabled)
        self._view.view_render_scene_options.cbShowNEE.blockSignals(False)
        path_index = self._model.current_path_index
        self._view.view_render_scene.scene_renderer.show_traced_path_nee(path_index, enabled)

    @Slot(bool, name='show_vertex_omega_o')
    def show_vertex_omega_o(self, enabled):
        """
        Informs the renderer to visualize the outgoing ray of the current selected vertex,
        depending on state
        :param enabled: boolean
        :return:
        """
        vertex_tpl = self._model.current_vertex_tpl
        self._view.view_render_scene.scene_renderer.show_vertex_omega_o(vertex_tpl, enabled)

    @Slot(bool, name='show_vertex_omega_i')
    def show_vertex_omega_i(self, enabled):
        """
        Informs the renderer to visualize the incoming ray of the current selected vertex,
        depending on state
        :param enabled: boolean
        :return:
        """
        vertex_tpl = self._model.current_vertex_tpl
        self._view.view_render_scene.scene_renderer.show_vertex_omega_i(vertex_tpl, enabled)

    @Slot(bool, name='show_vertex_nee')
    def show_vertex_nee(self, enabled):
        """
        Informs the renderer to visualize the next event estimation of the current selected vertex,
        depending on state
        :param enabled: boolean
        :return:
        """
        vertex_tpl = self._model.current_vertex_tpl
        self._view.view_render_scene.scene_renderer.show_vertex_nee(vertex_tpl, enabled)

    @Slot(bool, name='reset_all_paths_vertices')
    def reset_all_paths_vertices(self, clicked):
        """
        Informs the renderer to reset all path vertices
        :param clicked: boolean
        :return:
        """
        scene_renderer = self._view.view_render_scene.scene_renderer
        scene_renderer.reset_all_paths_vertices()
        tpl = self._model.current_vertex_tpl
        path_option_settings = scene_renderer.get_path_option_settings(tpl[0])
        self._view.view_render_scene_options.load_path_settings(path_option_settings)
        vertex_option_settings = scene_renderer.get_vertex_option_settings(tpl)
        self._view.view_render_scene_options.load_vertex_settings(vertex_option_settings)

    @Slot(bool, name='reset_path')
    def reset_path(self, clicked):
        """
        Informs the renderer to reset the paths size and opacity
        :param clicked: boolean
        :return:
        """
        scene_renderer = self._view.view_render_scene.scene_renderer
        scene_renderer.reset_path(self._model.current_path_index)
        path_settings = scene_renderer.get_path_option_settings(self._model.current_path_index)
        self._view.view_render_scene_options.load_path_settings(path_settings)

    @Slot(int, name='update_path_opacity')
    def update_path_opacity(self, opacity):
        """
        Informs the renderer to update the path opacity
        :param opacity: float[0,1]
        :return:
        """
        max_value = self._view.view_render_scene_options.sliderPathOpacity.maximum()
        path_index = self._model.current_path_index
        self._view.view_render_scene.scene_renderer.update_path_opacity(path_index, float(opacity / max_value))

    @Slot(int, name='update_path_size')
    def update_path_size(self, size):
        """
        Informs the renderer to update the path size
        :param size: float[0,1]
        :return:
        """
        path_index = self._model.current_path_index
        self._view.view_render_scene.scene_renderer.update_path_size(path_index, size)

    @Slot(int, name='update_vertex_opacity')
    def update_vertex_opacity(self, opacity):
        """
        Informs the renderer to update the vertex opacity of the current selected vertex
        :param opacity: float[0,1]
        :return:
        """
        max_value = self._view.view_render_scene_options.sliderVertexOpacity.maximum()
        vertex_tpl = self._model.current_vertex_tpl
        self._view.view_render_scene.scene_renderer.update_vertex_opacity(vertex_tpl, float(opacity / max_value))

    @Slot(int, name='update_vertex_size')
    def update_vertex_size(self, size):
        """
        Informs the renderer to update the vertex size of the current selected vertex
        :param size: float[0,1]
        :return:
        """
        vertex_tpl = self._model.current_vertex_tpl
        self._view.view_render_scene.scene_renderer.update_vertex_size(vertex_tpl, size)

    @Slot(bool, name='reset_vertex')
    def reset_vertex(self, clicked):
        """
        Informs the renderer to reset the vertex opacity and size
        :param clicked: boolean
        :return:
        """
        vertex_tpl = self._model.current_vertex_tpl
        self._view.view_render_scene.scene_renderer.reset_vertex(vertex_tpl)
        vertex_option_settings = self._view.view_render_scene.scene_renderer.get_vertex_option_settings(vertex_tpl)
        self._view.view_render_scene_options.load_vertex_settings(vertex_option_settings)
