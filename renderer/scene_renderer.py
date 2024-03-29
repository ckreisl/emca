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

from core.interface_scene import SceneInterface
from renderer.scene_geometry import SceneGeometry
from renderer.scene_traced_paths import SceneTracedPaths
from renderer.renderer import Renderer
import numpy as np
import threading
import logging


class SceneRenderer(SceneInterface):

    def __init__(self):
        super().__init__()
        self._scene_geometry = SceneGeometry(0.25)
        self._scene_traced_paths = SceneTracedPaths(1.0)
        self._renderer = Renderer()
        self._renderer.set_rubber_band_callback(self.rubber_band_selection)

        # Introduced to prevent multiple update calls while loading scene objects
        # Updating view is expensive
        self._widget_update_timer_running = False
        self._widget_update_timer = threading.Timer(0.1, self.widget_update_from_timer)

    @property
    def renderer(self):
        """
        Returns the renderer which renders the scene in a widget
        """
        return self._renderer

    @property
    def scene_geometry(self):
        """
        Returns the scene geometry object which keeps track of
        the camera and all meshes within the scene
        """
        return self._scene_geometry

    @property
    def scene_traced_paths(self):
        """
        Returns the scene traced paths objects which keeps track of
        all traced paths within the 3D scene
        """
        return self._scene_traced_paths

    @property
    def widget(self):
        """
        Returns the 3D render widget
        """
        return self._renderer.widget

    def rubber_band_selection(self, tpl):
        if tpl[0] in self._scene_traced_paths.paths:
            # same path select intersection
            if self._scene_traced_paths.prev_path.path_idx != tpl[0]:
                self.send_select_path(tpl[0])
            self.send_select_intersection(tpl)
        else:
            # some other path is selected update whole view
            self.send_update_path(np.array([tpl[0]]), False)
            self.send_select_path(tpl[0])
            self.send_select_intersection(tpl)

    def widget_update_from_timer(self):
        self.widget.update()
        self._widget_update_timer_running = False

    def update_path_indices(self, indices):
        current_indices = self._scene_traced_paths.path_indices
        # reset low opacity paths
        if len(current_indices) > 0:
            for key in current_indices:
                self._scene_traced_paths.paths[key].reset_path_opacity()
        self.remove_traced_paths_by_indices(self._scene_traced_paths.path_indices)
        self.display_traced_paths(indices)

    def select_path(self, index):
        for key in self._scene_traced_paths.path_indices:
            if key == index:
                path = self._scene_traced_paths.paths[key]
                if path.is_ne_visible:
                    path.draw_ne(self._renderer)
                if path.opacity != path.default_opacity:
                    path.set_path_opacity(path.default_opacity)
            else:
                self._scene_traced_paths.paths[key].set_path_opacity(0.25)
        self._scene_traced_paths.select_path(index)
        self.widget.update()

    def select_intersection(self, tpl):
        self._scene_traced_paths.select_intersection(tpl)
        path, intersection = self._scene_traced_paths.get_path_and_intersection(tpl)
        if intersection.is_ne_visible:
            intersection.draw_ne(self._renderer)
        if intersection.is_wi_visible:
            intersection.draw_wi(self._renderer)
        if intersection.is_wo_visible:
            intersection.draw_wo(self._renderer)
        if self._scene_geometry.camera.auto_clipping:
            if intersection:
                if intersection.pos:
                    self._scene_geometry.camera.set_focal_point(intersection.pos)
        self.widget.update()

    def remove_traced_paths_by_indices(self, indices):
        for key in indices:
            self._scene_traced_paths.paths[key].clear_all(self._renderer)

    def load_scene(self, camera_data, mesh_data):
        # currently not used ?!
        self.clear_scene_objects()
        self._scene_geometry.clear_scene_objects()
        self._scene_geometry.load_camera_data(camera_data)
        self._scene_geometry.load_scene_geometry(mesh_data)
        self._renderer.SetActiveCamera(self._scene_geometry.camera)
        for mesh in self._scene_geometry.meshes:
            self._renderer.AddActor(mesh)
        self.widget.update()

    def load_camera(self, camera_data):
        self._scene_geometry.load_camera_data(camera_data)
        self._renderer.SetActiveCamera(self._scene_geometry.camera)
        self.widget.update()

    def load_mesh(self, mesh_data):
        self._scene_geometry.add_mesh(mesh_data)
        self._renderer.AddActor(self._scene_geometry.meshes[-1])
        if not self._widget_update_timer_running:
            self._widget_update_timer_running = True
            self._widget_update_timer = threading.Timer(0.1, self.widget_update_from_timer)
            self._widget_update_timer.start()

    def load_traced_paths(self, render_data):
        # since prepare data is called before
        # we do not need to clear the paths twice from the scene
        self._scene_traced_paths.load_traced_paths(render_data)
        self.widget.update()

    def display_traced_paths(self, indices):
        self._scene_traced_paths.path_indices = indices
        for key in self._scene_traced_paths.path_indices:
            self._scene_traced_paths.paths[key].draw_path(self._renderer)
            self._scene_traced_paths.paths[key].draw_its(self._renderer)
        self.widget.update()

    def clear_scene_objects(self):
        for mesh in self._scene_geometry.meshes:
            self._renderer.RemoveActor(mesh)
        self.widget.update()

    def clear_traced_paths(self):
        for _, path in self._scene_traced_paths.paths.items():
            path.clear_all(self._renderer)
        self.widget.update()

    def reset_camera_position(self):
        self._scene_geometry.camera.reset()
        self.widget.update()

    def prepare_new_data(self):
        self.clear_traced_paths()
        self._scene_traced_paths.clear()

    # SCENE OPTIONS

    def get_path_option_settings(self, index):
        path = self._scene_traced_paths.paths[index]
        return {'all_paths_visible': self._scene_traced_paths.all_paths_visible,
                'all_nees_visible': self._scene_traced_paths.all_nees_visible,
                'opacity': path.opacity,
                'size': path.size,
                'is_visible': path.is_visible,
                'is_ne_visible': path.is_ne_visible}

    def get_intersection_option_settings(self, tpl):
        _, intersection = self._scene_traced_paths.get_path_and_intersection(tpl)
        return {'all_vertices_visible': self._scene_traced_paths.all_vertices_visible,
                'opacity': intersection.opacity,
                'size': intersection.size,
                'is_wi_visible': intersection.is_wi_visible,
                'is_wo_visible': intersection.is_wo_visible,
                'is_ne_visible': intersection.is_ne_visible}

    def get_camera_option_settings(self):
        camera = self._scene_geometry.camera
        return {'motion_speed': camera.motion_speed,
                'auto_clipping': camera.auto_clipping}

    def get_scene_option_settings(self):
        return {'scene_opacity': self._scene_geometry.scene_opacity}

    def apply_camera_option_settings(self, camera_settings):
        motion_speed = camera_settings.get('motion_speed', None)
        auto_clipping = camera_settings.get('auto_clipping', None)
        if motion_speed is not None:
            self._scene_geometry.camera.motion_speed = motion_speed
        if auto_clipping is not None:
            self._scene_geometry.camera.auto_clipping = auto_clipping
        self.widget.update()

    def reset_camera_option_settings(self):
        self._scene_geometry.camera.reset_motion_speed()
        self.widget.update()

    def apply_scene_option_settings(self, scene_settings):
        scene_opacity = scene_settings.get('scene_opacity', None)
        if scene_opacity is not None:
            self._scene_geometry.set_scene_opacity(scene_opacity)
        self.widget.update()

    def reset_scene_option_settings(self):
        self._scene_geometry.reset_scene_opacity()
        self.widget.update()

    def show_all_other_traced_paths(self, enable):
        current_indices = self._scene_traced_paths.path_indices
        all_indices = np.array(list(self._scene_traced_paths.paths.keys()))
        diff = np.setdiff1d(all_indices, current_indices)
        # reset low opacity paths
        if len(current_indices) > 1:
            for key, path in self._scene_traced_paths.paths.items():
                path.reset_path_opacity()
        if enable:
            # draw paths which are not yet visible
            for key in diff:
                self._scene_traced_paths.paths[key].draw_path(self._renderer)
        else:
            for key in diff:
                self._scene_traced_paths.paths[key].clear_path(self._renderer)
        self.widget.update()

    def show_all_other_traced_intersections(self, enable):
        is_all_verts_visible = self._scene_traced_paths.all_vertices_visible
        if enable:
            if not is_all_verts_visible:
                for path_idx, path in self._scene_traced_paths.paths.items():
                    if path_idx not in self._scene_traced_paths.path_indices:
                        for _, its in path.its_dict.items():
                            its.draw_its(self._renderer)
                self._scene_traced_paths.all_vertices_visible = not is_all_verts_visible
        else:
            if is_all_verts_visible:
                for path_idx, path in self._scene_traced_paths.paths.items():
                    if path_idx not in self._scene_traced_paths.path_indices:
                        for _, its in path.its_dict.items():
                            its.clear_its(self._renderer)
                self._scene_traced_paths.all_vertices_visible = not is_all_verts_visible
        self.widget.update()

    def show_traced_path(self, path_index, enable):
        path = self._scene_traced_paths.get_path(path_index)
        if enable:
            if not path.is_visible:
                path.draw_path(self._renderer)
                path.is_visible = True
        else:
            if path.is_visible:
                path.clear_path(self._renderer)
                path.is_visible = False
        self.widget.update()

    def update_path_opacity(self, path_index, opacity):
        path = self._scene_traced_paths.get_path(path_index)
        path.set_path_opacity(opacity)
        self.widget.update()

    def update_path_size(self, path_index, size):
        path = self._scene_traced_paths.get_path(path_index)
        path.set_path_size(size)
        self.widget.update()

    def reset_path(self, path_index):
        path = self._scene_traced_paths.get_path(path_index)
        path.reset_path_opacity()
        path.reset_path_size()
        self.widget.update()

    def show_all_traced_intersections(self, state):
        if state:
            for _, path in self._scene_traced_paths.paths.items():
                path.draw_its(self._renderer)
        else:
            for key, path in self._scene_traced_paths.paths.items():
                if key not in self._scene_traced_paths.path_indices:
                    path.clear_its(self._renderer)
        self.widget.update()

    def update_intersection_opacity(self, intersection_tpl, opacity):
        intersection = self._scene_traced_paths.get_intersection(intersection_tpl)
        intersection.set_intersection_opacity(opacity)
        self.widget.update()

    def update_intersection_size(self, intersection_tpl, size):
        intersection = self._scene_traced_paths.get_intersection(intersection_tpl)
        intersection.set_intersection_size(size)
        self.widget.update()

    def reset_intersection(self, intersection_tpl):
        intersection = self._scene_traced_paths.get_intersection(intersection_tpl)
        intersection.reset_intersection_opacity()
        intersection.reset_intersection_size()
        self.widget.update()

    def show_all_traced_nees(self, enabled):
        if enabled:
            for _, path in self._scene_traced_paths.paths.items():
                path.draw_ne(self._renderer)
        else:
            for _, path in self._scene_traced_paths.paths.items():
                path.clear_ne(self._renderer)
        self.widget.update()

    def show_traced_path_nee(self, path_index, enabled):
        for path_key in self._scene_traced_paths.path_indices:
            path = self._scene_traced_paths.paths.get(path_key, None)
            if path:
                if enabled:
                    if not path.is_ne_visible:
                        path.draw_ne(self._renderer)
                else:
                    if path.is_ne_visible:
                        path.clear_ne(self._renderer)
        self.widget.update()

    def show_intersection_omega_o(self, intersection_tpl, enabled):
        intersection = self._scene_traced_paths.get_intersection(intersection_tpl)
        if enabled:
            intersection.draw_wo(self._renderer)
        else:
            intersection.clear_wo(self._renderer)
        self.widget.update()

    def show_intersection_omega_i(self, intersection_tpl, enabled):
        intersection = self._scene_traced_paths.get_intersection(intersection_tpl)
        if enabled:
            intersection.draw_wi(self._renderer)
        else:
            intersection.clear_wi(self._renderer)
        self.widget.update()

    def show_intersection_nee(self, intersection_tpl, enabled):
        intersection = self._scene_traced_paths.get_intersection(intersection_tpl)
        if enabled:
            intersection.draw_ne(self._renderer)
        else:
            intersection.clear_ne(self._renderer)
        self.widget.update()

    def reset_all_paths_vertices(self):
        for _, path in self._scene_traced_paths.paths.items():
            path.reset_path_size()
            path.reset_path_opacity()
            path.reset_intersection_opacity()
            path.reset_intersection_size()
        self.widget.update()

    def draw_triangle(self, p1, p2, p3):
        return self._renderer.draw_triangle(p1, p2, p3)

    def draw_sphere(self, center, radius):
        return self._renderer.draw_sphere(center, radius)

    def draw_line(self, p1, p2):
        return self._renderer.draw_line(p1, p2)

    def draw_point(self, p1):
        return self._renderer.draw_point(p1)

    def remove_object(self, obj):
        return self._renderer.remove_object(obj)
