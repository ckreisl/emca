import logging


class RenderInterface(object):

    def __init__(self):
        self.view_render_scene = None
        self.view_render_scene_options = None

    def set_view_render_scene(self, view_render_scene):
        self.view_render_scene = view_render_scene

    def set_view_render_scene_options(self, view_render_scene_options):
        self.view_render_scene_options = view_render_scene_options

    def send_update_path(self, indices, add_item):
        self.view_render_scene.send_update_path(indices, add_item)

    def send_select_path(self, index):
        self.view_render_scene.send_select_path(index)

    def send_select_vertex(self, tpl):
        self.view_render_scene.send_select_vertex(tpl)
