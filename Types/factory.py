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
