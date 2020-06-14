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

from renderer.mesh import Mesh
from renderer.camera import Camera
import logging


class SceneGeometry(object):

    """
        Meshes
        Represents the list of vtkActors / Meshes within the scene
    """

    def __init__(self, opacity):
        self._camera = Camera()
        self._meshes = []
        self._default_scene_opacity = opacity
        self._scene_opacity = opacity

    @property
    def camera(self):
        """
        Returns the camera object
        """
        return self._camera

    @property
    def meshes(self):
        """
        Returns a list containing all meshes within the scene
        :return: list[Mesh, ...]
        """
        return self._meshes

    @property
    def scene_opacity(self):
        """
        Returns the default opacity value which is applied to all objects
        """
        return self._scene_opacity

    @property
    def mesh_count(self):
        """
        Amount of meshes in the scene
        :return: integer
        """
        return len(self._meshes)

    def create_mesh(self, mesh_data):
        mesh = Mesh(mesh_data)
        mesh.opacity = self._scene_opacity
        mesh.default_opacity = self._default_scene_opacity
        return mesh

    def set_scene_opacity(self, opacity):
        """
        Sets the opacity of all meshes in the scene
        :param opacity: float[0,1]
        :return:
        """
        for mesh in self._meshes:
            mesh.opacity = opacity
        self._scene_opacity = opacity

    def reset_scene_opacity(self):
        """
        Resets the opacity of all meshes to its default value (0.25)
        :return:
        """
        for mesh in self._meshes:
            mesh.opacity = self._default_scene_opacity
        self._scene_opacity = self._default_scene_opacity

    def add_mesh(self, mesh_data):
        """
        Adds a mesh to the mesh list
        :param mesh_data: Mesh object
        :return:
        """
        mesh = self.create_mesh(mesh_data)
        self._meshes.append(mesh)

    def load_camera_data(self, camera_data):
        """
        Initialises the camera settings with data from the model
        :param: camera_data
        :return:
        """
        self._camera.load_settings(camera_data)

    def load_scene_geometry(self, meshes_data):
        """
        Initialises and appends vtkMeshes to the mesh list,
        the data is loaded from the model.
        :param meshes_data: MeshData list from the model
        :return:
        """
        self._meshes.clear()
        for mesh_data in meshes_data.meshes:
            mesh = self.create_mesh(mesh_data)
            self._meshes.append(mesh)

    def clear_scene_objects(self):
        """
        Clears the list containing all meshes within the scene
        :return:
        """
        self._meshes.clear()
