from Renderer.mesh import Mesh
import logging


class Meshes(object):

    """
        Meshes
        Represents the list of vtkActors / Meshes within the scene
    """

    def __init__(self):
        self._meshes = []
        self._opacity = 0.25

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

    @property
    def opacity(self):
        """
        Returns the default opacity of all meshes 0.25
        :return: float[0,1]
        """
        return self._opacity

    @opacity.setter
    def opacity(self, new_opacity):
        """
        Sets the opacity
        :param new_opacity: float[0,1]
        :return:
        """
        self._opacity = new_opacity

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
            mesh.set_opacity(self._opacity)

    def add_mesh(self, mesh_data):
        """
        Adds a mesh to the mesh list
        :param mesh_data: Mesh object
        :return:
        """
        self._meshes.append(Mesh(mesh_data, self._opacity))

    def load_from_mesh_data(self, meshes):
        """
        Initialises and appends vtkMeshes to the mesh list,
        the data is loaded from the model.
        :param meshes: Mesh list from the model
        :return:
        """
        self._meshes.clear()
        for mesh_data in meshes.meshes:
            self._meshes.append(Mesh(mesh_data, self._opacity))

    def clear(self):
        """
        Clears the list containing all meshes within the scene
        :return:
        """
        self._meshes.clear()
