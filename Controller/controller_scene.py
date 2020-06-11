from Core.messages import StateMsg


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
