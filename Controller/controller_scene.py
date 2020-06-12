from Core.messages import StateMsg
import numpy as np


class ControllerRenderScene(object):

    def __init__(self, parent, model, view):
        self._controller_main = parent
        self._model = model
        self._view = view

    def init_scene_renderer(self, scene_renderer):
        scene_renderer.set_view_render_scene(self._view.view_render_scene)
        scene_renderer.set_view_render_scene_options(self._view.view_render_scene_options)
        self._view.view_render_scene.init_scene_renderer(scene_renderer)

    def handle_state_msg(self, tpl):
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
        elif msg is StateMsg.DATA_MESH:
            # TODO check comment above
            self._view.view_render_scene.load_mesh(tpl[1])

    def show_all_traced_vertices(self, enabled):
        self._view.view_render_scene.scene_renderer.show_all_traced_vertices(enabled)

    def show_all_other_traced_vertices(self, enabled):
        self._view.view_render_scene.scene_renderer.show_all_other_traced_vertices(enabled)

    def show_all_traced_nees(self, enabled):
        # NE checkbox path
        self._view.view_render_scene_options.cbShowNEERays.blockSignals(True)
        self._view.view_render_scene_options.cbShowNEERays.setChecked(enabled)
        self._view.view_render_scene_options.cbShowNEERays.blockSignals(False)
        # NE checkbox vertex / intersection
        self._view.view_render_scene_options.cbShowNEE.blockSignals(True)
        self._view.view_render_scene_options.cbShowNEE.setChecked(enabled)
        self._view.view_render_scene_options.cbShowNEE.blockSignals(False)
        self._view.view_render_scene.scene_renderer.show_all_traced_nees(enabled)

    def show_traced_path_nee(self, enabled):
        # toggle also vertex nee checkbox
        self._view.view_render_scene_options.cbShowNEE.blockSignals(True)
        self._view.view_render_scene_options.cbShowNEE.setChecked(enabled)
        self._view.view_render_scene_options.cbShowNEE.blockSignals(False)
        self._view.view_render_scene.scene_renderer.show_traced_path_nee(enabled)

    def show_vertex_omega_o(self, enabled):
        self._view.view_render_scene.scene_renderer.show_vertex_omega_o(enabled)

    def show_vertex_omega_i(self, enabled):
        self._view.view_render_scene.scene_renderer.show_vertex_omega_i(enabled)

    def show_vertex_nee(self, enabled):
        self._view.view_render_scene.scene_renderer.show_vertex_nee(enabled)

    def reset_all_paths_vertices(self, clicked):
        scene_renderer = self._view.view_render_scene.scene_renderer
        scene_renderer.reset_all_paths_vertices()
        tpl = self._controller_main.vertex_index
        path_option_settings = scene_renderer.get_path_option_settings(tpl[0])
        self._view.view_render_scene_options.load_path_settings(path_option_settings)
        vertex_option_settings = scene_renderer.get_vertex_option_settings(tpl)
        self._view.view_render_scene_options.load_vertex_settings(vertex_option_settings)
