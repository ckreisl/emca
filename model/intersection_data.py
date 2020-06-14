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

from model.user_data import UserData
import logging


class IntersectionData(UserData):

    """
        IntersectionData
        Represents one intersection point of a traced path through the scene.
        Holds information about the intersection, more precisely the vertex position, the vertex index,
        if a next event estimation was set, if a vertex position was set and current estimate information at this point.
    """

    def __init__(self):
        UserData.__init__(self)
        self._depth_idx = None
        self._pos = None
        self._set_pos = None
        self._occluded_ne = None
        self._set_ne = None
        self._pos_ne = None
        self._occluded_ne = None
        self._pos_envmap = None
        self._set_envmap = None
        self._li = None
        self._set_li = None

    def deserialize(self, stream):
        """
        Deserialize a IntersectionData object from the socket stream
        :param stream:
        :return:
        """
        super().deserialize(stream)
        self._depth_idx = stream.read_int()

        self._pos = None
        self._set_pos = stream.read_bool()
        if self._set_pos:
            self._pos = stream.read_point3f()

        self._pos_ne = None
        self._occluded_ne = None
        self._set_ne = stream.read_bool()
        if self._set_ne:
            self._pos_ne = stream.read_point3f()
            self._occluded_ne = stream.read_bool()

        self._pos_envmap = None
        self._set_envmap = stream.read_bool()
        if self._set_envmap:
            self._pos_envmap = stream.read_point3f()

        self._li = None
        self._set_li = stream.read_bool()
        if self._set_li:
            self._li = stream.read_color3f()

    @property
    def depth_idx(self):
        """
        Returns the current depth index (vertex index)
        :return: integer
        """
        return self._depth_idx

    @property
    def is_pos_set(self):
        """
        Returns if a intersection position was set on the server side
        :return: boolean
        """
        return self._set_pos

    @property
    def is_ne_set(self):
        """
        Returns if a next event estimation was set on the server side
        :return: boolean
        """
        return self._set_ne

    @property
    def is_ne_occluded(self):
        """
        Returns if the next estimation is occluded
        :return: boolean
        """
        return self._occluded_ne

    @property
    def is_envmap_set(self):
        """
        Returns of a environment map position was set on the server
        :return: boolean
        """
        return self._set_envmap

    @property
    def is_li_set(self):
        """
        Returns if a current estimate at this position was set on the server
        :return: color3f
        """
        return self._set_li

    @property
    def pos(self):
        """
        Returns the vertex / intersection position
        :return: point3f
        """
        return self._pos

    @property
    def pos_ne(self):
        """
        Returns the position of the next event estimation
        :return: point3f
        """
        return self._pos_ne

    @property
    def pos_envmap(self):
        """
        Returns the position on the environment map
        :return:
        """
        return self._pos_envmap

    @property
    def li(self):
        """
        Returns the current estimate at this intersection / path position
        :return:
        """
        return self._li

