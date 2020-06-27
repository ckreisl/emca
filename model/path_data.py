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

from model.intersection_data import IntersectionData
from model.user_data import UserData
import logging


class PathData(UserData):

    """
        PathData
        Represents one traced path with added user data
    """

    def __init__(self):
        super().__init__()

        self._sample_idx = -1
        self._path_depth = -1
        self._path_origin = None
        self._final_estimate = None
        self._show_path = False
        self._show_ne = False
        self._dict_intersections = {}
        self._intersection_count = 0

    def deserialize(self, stream):
        """
        Deserializes one path object from the socket stream
        :param stream:
        :return:
        """
        super().deserialize(stream)
        self._sample_idx = stream.read_int()
        self._path_depth = stream.read_int()
        self._path_origin = stream.read_point3f()

        self._final_estimate = None
        if stream.read_bool():
            self._final_estimate = stream.read_color3f()

        self._show_path = stream.read_bool()
        self._show_ne = stream.read_bool()

        self._dict_intersections.clear()
        self._intersection_count = stream.read_uint()
        for i in range(0, self._intersection_count):
            intersection_index = stream.read_int()
            intersection = IntersectionData()
            intersection.deserialize(stream)
            self._dict_intersections[intersection_index] = intersection

    @property
    def final_estimate(self):
        """
        Returns the Final Estimate value of this path
        :return: color3f
        """
        return self._final_estimate

    @property
    def sample_idx(self):
        """
        Returns the samples index which indicates the path index
        :return: integer
        """
        return self._sample_idx

    @property
    def path_origin(self):
        """
        Returns the path origin
        :return: point3f
        """
        return self._path_origin

    @property
    def path_depth(self):
        """
        Returns the path depth (amount of bounces and containing vertices)
        :return: integer
        """
        return self._path_depth

    @property
    def intersections(self):
        """
        Returns the a dict containing all path vertices
        :return: dict{intersection_idx, intersection object}
        """
        return self._dict_intersections

    @property
    def is_show_path(self):
        """
        Returns if intersection points were added
        :return: boolean
        """
        return self._show_path

    @property
    def is_show_ne(self):
        """
        Returns if next event estimation was added
        :return: boolean
        """
        return self._show_ne

    @property
    def intersection_count(self):
        """
        Returns the amount of vertices (intersections)
        :return: integer
        """
        return self._intersection_count

    def valid_depth(self):
        """
        Checks if the path depth is valid (path_depth != -1)
        :return: bool
        """
        return self._path_depth != -1
