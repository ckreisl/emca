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
        self._view.view_render_scene.scene_renderer.reset_camera_position()

    def update_camera_motion_speed(self, speed):
        self._view.view_render_scene.scene_renderer.apply_camera_option_settings({'motion_speed': speed})

    def update_camera_clipping(self, enabled):
        self._view.view_render_scene.scene_renderer.apply_camera_option_settings({'auto_clipping': enabled})

    def reset_camera_motion_speed(self, clicked):
        scene_renderer = self._view.view_render_scene.scene_renderer
        scene_renderer.reset_camera_option_settings()
        camera_settings = scene_renderer.get_camera_option_settings()
        self._view.view_render_scene_options.load_camera_settings(camera_settings)

    def update_scene_opacity(self, opacity):
        max_value = self._view.view_render_scene_options.sliderMeshOpacity.maximum()
        self._view.view_render_scene.apply_scene_option_settings({'scene_opacity': float(opacity / max_value)})

    def reset_scene(self, clicked):
        scene_renderer = self._view.view_render_scene.scene_renderer
        scene_renderer.reset_scene_option_settings()
        scene_settings = scene_renderer.get_scene_option_settings()
        self._view.view_render_scene_options.load_scene_settings(scene_settings)

    def update_mesh_opacity(self, opacity):
        # todo
        pass

    def reset_mesh(self, clicked):
        # todo
        pass

    def inspect_selected_path(self, clicked):
        index = np.array([self._model.current_path_index])
        self._controller_main.update_path(index, False)

    def show_traced_path(self, enabled):
        # toggle also vertex omega_i checkbox
        self._view.view_render_scene_options.cbShowOmegaI.blockSignals(True)
        self._view.view_render_scene_options.cbShowOmegaI.setChecked(enabled)
        self._view.view_render_scene_options.cbShowOmegaI.blockSignals(False)
        path_index = self._model.current_path_index
        self._view.view_render_scene.scene_renderer.show_traced_path(path_index, enabled)

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

    def show_all_other_traced_paths(self, enabled):
        self._view.view_render_scene.scene_renderer.show_all_other_traced_paths(enabled)

    def show_traced_path_nee(self, enabled):
        # toggle also vertex nee checkbox
        self._view.view_render_scene_options.cbShowNEE.blockSignals(True)
        self._view.view_render_scene_options.cbShowNEE.setChecked(enabled)
        self._view.view_render_scene_options.cbShowNEE.blockSignals(False)
        path_index = self._model.current_path_index
        self._view.view_render_scene.scene_renderer.show_traced_path_nee(path_index, enabled)

    def show_vertex_omega_o(self, enabled):
        vertex_tpl = self._model.current_vertex_tpl
        self._view.view_render_scene.scene_renderer.show_vertex_omega_o(vertex_tpl, enabled)

    def show_vertex_omega_i(self, enabled):
        vertex_tpl = self._model.current_vertex_tpl
        self._view.view_render_scene.scene_renderer.show_vertex_omega_i(vertex_tpl, enabled)

    def show_vertex_nee(self, enabled):
        vertex_tpl = self._model.current_vertex_tpl
        self._view.view_render_scene.scene_renderer.show_vertex_nee(vertex_tpl, enabled)

    def reset_all_paths_vertices(self, clicked):
        scene_renderer = self._view.view_render_scene.scene_renderer
        scene_renderer.reset_all_paths_vertices()
        tpl = self._controller_main.vertex_index
        path_option_settings = scene_renderer.get_path_option_settings(tpl[0])
        self._view.view_render_scene_options.load_path_settings(path_option_settings)
        vertex_option_settings = scene_renderer.get_vertex_option_settings(tpl)
        self._view.view_render_scene_options.load_vertex_settings(vertex_option_settings)

    def reset_path(self, clicked):
        scene_renderer = self._view.view_render_scene.scene_renderer
        scene_renderer.reset_path(self._model.current_path_index)
        path_settings = scene_renderer.get_path_option_settings(self._model.current_path_index)
        self._view.view_render_scene_options.load_path_settings(path_settings)

    def update_path_opacity(self, opacity):
        max_value = self._view.view_render_scene_options.sliderPathOpacity.maximum()
        path_index = self._model.current_path_index
        self._view.view_render_scene.scene_renderer.update_path_opacity(path_index, float(opacity / max_value))

    def update_path_size(self, size):
        path_index = self._model.current_path_index
        self._view.view_render_scene.scene_renderer.update_path_size(path_index, size)

    def update_vertex_opacity(self, opacity):
        max_value = self._view.view_render_scene_options.sliderVertexOpacity.maximum()
        vertex_tpl = self._model.current_vertex_tpl
        self._view.view_render_scene.scene_renderer.update_vertex_opacity(vertex_tpl, float(opacity / max_value))

    def update_vertex_size(self, size):
        vertex_tpl = self._model.current_vertex_tpl
        self._view.view_render_scene.scene_renderer.update_vertex_size(vertex_tpl, size)

    def reset_vertex(self, clicked):
        vertex_tpl = self._model.current_vertex_tpl
        self._view.view_render_scene.scene_renderer.reset_vertex(vertex_tpl)
        vertex_option_settings = self._view.view_render_scene.scene_renderer.get_vertex_option_settings(vertex_tpl)
        self._view.view_render_scene_options.load_vertex_settings(vertex_option_settings)
