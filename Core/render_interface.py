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
