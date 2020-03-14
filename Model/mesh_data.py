"""
    This file is part of EMCA, an explorer of Monte-Carlo based Algorithms.
    Copyright (c) 2019-2020 by Christoph Kreisl and others.
    EMCA is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License Version 3
    as published by the Free Software Foundation.
    EMCA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from Types.factory import TypeFactory
from Types.color3 import Color3f
import logging

import numpy as np


class Mesh(object):

    """
        Mesh
        This class represents one three-dimensional mesh object,
        consisting of vertices and triangle indices a specular and diffuse color.
    """

    def __init__(self):
        self._vertex_count = None
        self._vertices = np.array([], 'f')

        self._triangle_count = None
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
        triangleIndices = np.array(stream.read_int_array(self._triangle_count*3), 'q')
        self._triangles = np.concatenate([np.full([self._triangle_count, 1], 3, 'q'), triangleIndices.reshape([self._triangle_count, 3])], axis=1).flatten()

        # remember we got the alpha channel!
        self._specular_color = stream.read_color3f()
        self._diffuse_color = stream.read_color3f()

    def deserialize_xml(self, node):
        """
        Deserialize a Mesh object from a xml file
        :param node:
        :return:
        """
        self._triangles.clear()
        self._vertices.clear()
        for item in list(node):
            if item.tag == "integer" and item.attrib["name"] == "vertexCount":
                self._vertex_count = int(item.text)
            elif item.tag == "point3f" and item.attrib["name"] == "vertex":
                self._vertices.append(TypeFactory.create_point3f_from_str(item.text))
            elif item.tag == "integer" and item.attrib["name"] == "triangleCount":
                self._triangle_count = int(item.text)
            elif item.tag == "point3i" and item.attrib["name"] == "triangleIndices":
                self._triangles.append(TypeFactory.create_point3i_from_str(item.text))
            elif item.tag == "color3f" and item.attrib["name"] == "specular":
                self._specular_color = TypeFactory.create_color3f_from_str(item.text)
            elif item.tag == "color3f" and item.attrib["name"] == "diffuse":
                self._diffuse_color = TypeFactory.create_color3f_from_str(item.text)

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
        :return:
        """
        return 'vertexCount = {} \n' \
               'triangleCount = {} \n' \
               'specularColor = {} \n' \
               'diffuseColor = {} \n'.format(self._vertex_count,
                                             self._triangle_count,
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
        mesh = Mesh()
        mesh.deserialize(stream)
        self._meshes.append(mesh)

    def deserialize_xml(self, node):
        """
        Deserializes a mesh object from a xml file and appends it to the overall mesh list
        :param node:
        :return:
        """
        self._meshes.clear()
        for item in list(node):
            if item.tag == "mesh":
                mesh = Mesh()
                mesh.deserialize_xml(item)
                self._meshes.append(mesh)

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
        :return:
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
