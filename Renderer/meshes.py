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

from Renderer.mesh import Mesh
import logging


class Meshes(object):

    """
        Meshes
        Represents the list of vtkActors / Meshes within the scene
    """

    def __init__(self):
        self._meshes = []

    @property
    def mesh_count(self):
        """
        Amount of meshes in the scene
        :return: integer
        """
        return len(self._meshes)

    @property
    def meshes(self):
        """
        Returns a list containing all meshes within the scene
        :return: list[Mesh, ...]
        """
        return self._meshes

    def set_opacity(self, opacity):
        """
        Sets the opacity of all meshes in the scene
        :param opacity: float[0,1]
        :return:
        """
        for mesh in self._meshes:
            mesh.set_opacity(opacity)

    def reset_opacity(self):
        """
        Resets the opacity of all meshes to its default value (0.25)
        :return:
        """
        for mesh in self._meshes:
            mesh.reset_opacity()

    def add_mesh(self, mesh_data):
        """
        Adds a mesh to the mesh list
        :param mesh_data: Mesh object
        :return:
        """
        self._meshes.append(Mesh(mesh_data))

    def load_from_mesh_data(self, meshes):
        """
        Initialises and appends vtkMeshes to the mesh list,
        the data is loaded from the model.
        :param meshes: Mesh list from the model
        :return:
        """
        self._meshes.clear()
        for mesh_data in meshes.meshes:
            self._meshes.append(Mesh(mesh_data))

    def clear(self):
        """
        Clears the list containing all meshes within the scene
        :return:
        """
        self._meshes.clear()
