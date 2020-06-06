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

from Core.scene_interface import SceneInterface
from Renderer.scene_geometry import SceneGeometry
from Renderer.scene_traced_paths import SceneTracedPaths
from Renderer.renderer import Renderer
import threading
import logging


class SceneRenderer(SceneInterface):

    def __init__(self):
        super().__init__()
        self._renderer = Renderer()
        self._scene_geometry = SceneGeometry(0.25)
        self._scene_traced_paths = SceneTracedPaths(1.0)

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

    def widget_update_from_timer(self):
        self.widget.update()
        self._widget_update_timer_running = False

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
        self._scene_traced_paths.display_traced_paths(indices)
        # TODO think about other method to load path
        # do not hand over renderer to render stuff ?!
        # ----------------- DEBUG START
        logging.info(self._scene_traced_paths.paths)
        logging.info(self._scene_traced_paths.path_indices)
        # ----------------- DEBUG END
        for key in self._scene_traced_paths.path_indices:
            self._scene_traced_paths.paths[key].draw_path(self._renderer)
            self._scene_traced_paths.paths[key].draw_verts(self._renderer)
        self.widget.update()

    def clear_scene_objects(self):
        for mesh in self._scene_geometry.meshes:
            self._renderer.RemoveActor(mesh)
        self.widget.update()

    def clear_traced_paths(self):
        for _, path in self._scene_traced_paths.paths.items():
            self._renderer.RemoveActor(path)
        self.widget.update()

    def reset_camera_position(self):
        self._scene_geometry.camera.reset()
        self.widget.update()

    def prepare_new_data(self):
        self.clear_traced_paths()
        self._scene_traced_paths.reset()
