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

from Types.color3 import Color3f
from Types.point3 import Point3f
from Types.point3 import Point3i
from Types.point2 import Point2f
from Types.point2 import Point2i
from Types.vector3 import Vec3f
from Types.vector3 import Vec3i
from Types.vector2 import Vec2i
from Types.vector2 import Vec2f


class TypeFactory(object):

    """
        TypeFactory
        Is used to convert a string to a point, vector or color class type,
        used when reading / loading a xml file.
    """

    def __init__(self):
        pass

    @staticmethod
    def to_string(obj):
        if obj:
            return obj.to_string()
        else:
            return 'None'

    @staticmethod
    def clean_str(string):
        return string.replace("[", "").replace("]", "").replace(" ", "").split(",")

    @staticmethod
    def create_boolean_from_str(string):
        return string == "True"

    @staticmethod
    def create_color3f_from_str(string):
        s = TypeFactory.clean_str(string)
        if len(s) == 4:
            return Color3f(s[0], s[1], s[2], s[3])
        return None

    @staticmethod
    def create_point3f_from_str(string):
        s = TypeFactory.clean_str(string)
        if len(s) == 3:
            return Point3f(s[0], s[1], s[2])
        return None

    @staticmethod
    def create_point3i_from_str(string):
        s = TypeFactory.clean_str(string)
        if len(s) == 3:
            return Point3i(s[0], s[1], s[2])
        return None

    @staticmethod
    def create_point2f_from_str(string):
        s = TypeFactory.clean_str(string)
        if len(s) == 2:
            return Point2f(s[0], s[1])
        return None

    @staticmethod
    def create_point2i_from_str(string):
        s = TypeFactory.clean_str(string)
        if len(s) == 2:
            return Point2i(s[0], s[1])
        return None

    @staticmethod
    def create_vec3f_from_str(string):
        s = TypeFactory.clean_str(string)
        if len(s) == 3:
            return Vec3f(s[0], s[1], s[2])
        return None

    @staticmethod
    def create_vec3i_from_str(string):
        s = TypeFactory.clean_str(string)
        if len(s) == 3:
            return Vec3i(s[0], s[1], s[2])
        return None

    @staticmethod
    def create_vec2f_from_str(string):
        s = TypeFactory.clean_str(string)
        if len(s) == 2:
            return Vec2f(s[0], s[1])
        return None

    @staticmethod
    def create_vec2i_from_str(string):
        s = TypeFactory.clean_str(string)
        if len(s) == 2:
            return Vec2i(s[0], s[1])
        return None
