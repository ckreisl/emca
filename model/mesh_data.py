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

from core.color3 import Color3f
from core.point3 import Point3f
from core.messages import MeshType

import numpy as np
import logging


class Mesh(object):

    """
        Mesh
        This class represents one three-dimensional mesh object,
        consisting of vertices and triangle indices a specular and diffuse color.
    """

    def __init__(self):
        self._mesh_type = MeshType.TriangleMesh
        self._vertex_count = 0
        self._vertices = np.array([], 'f')

        self._triangle_count = 0
        self._triangles = np.array([], 'q')

        self._specular_color = Color3f()
        self._diffuse_color = Color3f()

    def deserialize(self, stream):
        """
        Deserialize a Mesh object from the socket stream.
        :param stream:
        :return:
        """

        self._vertex_count = stream.read_uint()
        self._vertices = np.array(stream.read_float_array(self._vertex_count*3), 'f')

        self._triangle_count = stream.read_uint()
        triangle_indices = np.array(stream.read_int_array(self._triangle_count*3), 'q')
        self._triangles = np.concatenate([np.full([self._triangle_count, 1], 3, 'q'),
                                          triangle_indices.reshape([self._triangle_count, 3])], axis=1).flatten()

        # remember we got the alpha channel!
        self._specular_color = stream.read_color3f()
        self._diffuse_color = stream.read_color3f()

    @property
    def mesh_type(self):
        return self._mesh_type

    @property
    def vertex_count(self):
        """
        Returns the amount of vertices of this mesh
        :return: integer
        """
        return self._vertex_count

    @property
    def vertices(self):
        """
        Returns a list containing all vertices (point3f list)
        :return: list[point3f]
        """
        return self._vertices

    @property
    def triangle_count(self):
        """
        Returns the amount of triangles
        :return: integer
        """
        return self._triangle_count

    @property
    def triangles(self):
        """
        Returns a list containing all triangles indices (point3i list)
        :return: list[point3i,...]
        """
        return self._triangles

    @property
    def specular_color(self):
        """
        Returns the specular color of the mesh object
        :return: color3f
        """
        return self._specular_color

    @property
    def diffuse_color(self):
        """
        Returns the diffuse color of the mesh object
        :return: color3f
        """
        return self._diffuse_color

    def to_string(self):
        """
        Returns a string containing all information about the Mesh object
        :return: str
        """
        return 'vertexCount = {} \n' \
               'triangleCount = {} \n' \
               'specularColor = {} \n' \
               'diffuseColor = {} \n'.format(self._vertex_count,
                                             self._triangle_count,
                                             self._specular_color.to_string(),
                                             self._diffuse_color.to_string())


class Sphere(object):

    """
        Sphere
        This class represents one three-dimensional sphere object,
    """

    def __init__(self):
        self._mesh_type = MeshType.SphereMesh
        self._radius = 1.0
        self._center = Point3f()
        self._specular_color = Color3f()
        self._diffuse_color = Color3f()

    def deserialize(self, stream):
        """
        Deserialize a Sphere object from the socket stream.
        :param stream:
        :return:
        """
        self._radius = stream.read_float()
        self._center = stream.read_point3f()
        # remember we got the alpha channel!
        self._diffuse_color = stream.read_color3f()
        self._specular_color = stream.read_color3f()

    @property
    def mesh_type(self):
        return self._mesh_type

    @property
    def radius(self):
        """
        Returns the radius of the sphere
        :return: float
        """
        return self._radius

    @property
    def center(self):
        """
        Return the center point of the sphere
        :return: Point3f
        """
        return self._center

    @property
    def specular_color(self):
        """
        Returns the specular color of the mesh object
        :return: color3f
        """
        return self._specular_color

    @property
    def diffuse_color(self):
        """
        Returns the diffuse color of the mesh object
        :return: color3f
        """
        return self._diffuse_color

    def to_string(self):
        """
        Returns a string containing all information about the Mesh object
        :return: str
        """
        return 'radius = {} \n' \
               'center = {} \n' \
               'specularColor = {} \n' \
               'diffuseColor = {} \n'.format(self._radius,
                                             self._center,
                                             self._specular_color.to_string(),
                                             self._diffuse_color.to_string())


class MeshData(object):

    """
        MeshData
        Holds all Mesh objects which are in the 3D scene
    """

    def __init__(self):
        self._meshes = []

    def deserialize(self, stream):
        """
        Deserializes a mesh object from the socket stream and appends it to the overall mesh list
        :param stream:
        :return:
        """
        mesh_type = stream.read_short()
        logging.info("MeshType: {}".format(mesh_type))
        if mesh_type == MeshType.TriangleMesh.value:
            mesh = Mesh()
            mesh.deserialize(stream)
            self._meshes.append(mesh)
        elif mesh_type == MeshType.SphereMesh.value:
            sphere = Sphere()
            sphere.deserialize(stream)
            self._meshes.append(sphere)

    @property
    def mesh_count(self):
        """
        Returns the amount of objects in the 3D scene
        :return: integer
        """
        return len(self._meshes)

    @property
    def meshes(self):
        """
        Returns the list of objects
        :return: list[mesh,...]
        """
        return self._meshes

    def to_string(self):
        """
        Returns a string with information about all mesh objects
        :return: str
        """
        oss = 'meshCount = {} \n'.format(len(self._meshes))
        for mesh in self._meshes:
            oss = oss + "Mesh = { \n" + mesh.to_string() + "} \n \n"
        return oss

    def clear(self):
        """
        Clears the list of all mesh objects
        :return:
        """
        self._meshes.clear()
