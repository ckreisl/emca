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
from Types.vector3 import Vec3f
from Types.point3 import Point3f
import logging


class CameraData(object):

    """
        Camera Data
        Holds information about the camera data
        Will be used by the renderer interface to initialise the camera for the 3D scene viewer
    """

    def __init__(self):
        self._near_clip = None
        self._far_clip = None
        self._focus_dist = None
        self._fov = None
        self._up = Vec3f()
        self._direction = Vec3f()
        self._origin = Point3f()

    def deserialize(self, stream):
        """
        Deserializes all camera information from the socket stream
        :param stream:
        :return:
        """
        self._near_clip = stream.read_float()
        self._far_clip = stream.read_float()
        self._focus_dist = stream.read_float()
        self._fov = stream.read_float()
        self._up = stream.read_vec3f()
        self._direction = stream.read_vec3f()
        self._origin = stream.read_point3f()

    def deserialize_xml(self, node):
        """
        Deserializes all camera information from the xml file
        :param node:
        :return:
        """
        for item in list(node):
            if item.tag == "float" and item.attrib["name"] == "nearClip":
                self._near_clip = float(item.text)
            elif item.tag == "float" and item.attrib["name"] == "farClip":
                self._far_clip = float(item.text)
            elif item.tag == "float" and item.attrib["name"] == "focusDist":
                self._focus_dist = float(item.text)
            elif item.tag == "float" and item.attrib["name"] == "fov":
                self._fov = float(item.text)
            elif item.tag == "vec3f" and item.attrib["name"] == "viewUp":
                self._up = TypeFactory.create_vec3f_from_str(item.text)
            elif item.tag == "vec3f" and item.attrib["name"] == "viewDirection":
                self._direction = TypeFactory.create_vec3f_from_str(item.text)
            elif item.tag == "point3f" and item.attrib["name"] == "origin":
                self._origin = TypeFactory.create_point3f_from_str(item.text)

    @property
    def near_clip(self):
        """
        Returns the camera near clip value
        :return:
        """
        return self._near_clip

    @property
    def far_clip(self):
        """
        Returns the camera far clip value
        :return:
        """
        return self._far_clip

    @property
    def focus_dist(self):
        """
        Returns the camera focus distance
        :return:
        """
        return self._focus_dist

    @property
    def fov(self):
        """
        Returns the camera the field of view angle
        :return:
        """
        return self._fov

    @property
    def up(self):
        """
        Returns the camera up vector
        :return:
        """
        return self._up

    @property
    def direction(self):
        """
        Returns the camera viewing direction
        :return:
        """
        return self._direction

    @property
    def origin(self):
        """
        Returns the camera 3D origin world point
        :return:
        """
        return self._origin

    def to_string(self):
        """
        Returns all camera information within a string
        :return:
        """
        return 'neaClip = {} \n' \
               'farClip = {} \n' \
               'focusDist = {} \n' \
               'fov = {} \n' \
               'up = {} \n' \
               'direction = {} \n' \
               'origin = {} \n'.format(self._near_clip,
                                       self._far_clip,
                                       self._focus_dist,
                                       self._fov,
                                       self._up.to_string(),
                                       self._direction.to_string(),
                                       self._origin.to_string())


