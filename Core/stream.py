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
from Types.vector2 import Vec2f
from Types.vector2 import Vec2i
from Types.vector3 import Vec3i
from Types.vector3 import Vec3f
from Types.point2 import Point2f
from Types.point2 import Point2i
from Types.point3 import Point3f
from Types.point3 import Point3i

import abc
import struct
from enum import Enum
import logging


class ByteOrder(Enum):
    NATIVE              = '@'   # native
    LITTLE_ENDIAN       = '<'   # little endian
    BIG_ENDIAN          = '>'   # big endian
    NETWORK             = '!'   # network (= big endian)


class Format(Enum):
    CHAR                = 'c'
    SIGNED_CHAR         = 'b'
    UNSIGNED_CHAR       = 'B'
    BOOL                = '?'
    SHORT               = 'h'
    UNSIGNED_SHORT      = 'H'
    INT                 = 'i'
    UNSIGNED_INT        = 'I'
    LONG                = 'l'
    UNSIGNED_LONG       = 'L'
    LONG_LONG           = 'q'
    UNSIGNED_LONG_LONG  = 'Q'
    FLOAT               = 'f'
    DOUBLE              = 'd'


class SizeOf(Enum):
    CHAR                = struct.calcsize(Format.CHAR.value)
    SIGNED_CHAR         = struct.calcsize(Format.UNSIGNED_CHAR.value)
    UNSIGNED_CHAR       = struct.calcsize(Format.UNSIGNED_CHAR.value)
    BOOL                = struct.calcsize(Format.BOOL.value)
    SHORT               = struct.calcsize(Format.SHORT.value)
    UNSIGNED_SHORT      = struct.calcsize(Format.UNSIGNED_SHORT.value)
    INT                 = struct.calcsize(Format.INT.value)
    UNSIGNED_INT        = struct.calcsize(Format.UNSIGNED_INT.value)
    LONG                = struct.calcsize(Format.LONG.value)
    UNSIGNED_LONG       = struct.calcsize(Format.UNSIGNED_LONG.value)
    LONG_LONG           = struct.calcsize(Format.LONG_LONG.value)
    UNSIGNED_LONG_LONG  = struct.calcsize(Format.UNSIGNED_LONG_LONG.value)
    FLOAT               = struct.calcsize(Format.FLOAT.value)
    DOUBLE              = struct.calcsize(Format.DOUBLE.value)


class Stream(object):

    """
    Stream interface
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def read(self, size):
        return

    @abc.abstractmethod
    def write(self, data, size):
        return

    """ Write operations """

    def write_char(self, value):
        data = struct.pack(Format.CHAR.value, value)
        self.write(data, SizeOf.CHAR.value)

    def write_schar(self, value):
        data = struct.pack(Format.UNSIGNED_CHAR.value, value)
        self.write(data, SizeOf.SIGNED_CHAR.value)

    def write_uchar(self, value):
        data = struct.pack(Format.UNSIGNED_CHAR.value, value)
        self.write(data, SizeOf.UNSIGNED_CHAR.value)

    def write_bool(self, value):
        data = struct.pack(Format.BOOL.value, value)
        self.write(data, SizeOf.BOOL.value)

    def write_short(self, value):
        data = struct.pack(Format.SHORT.value, value)
        self.write(data, SizeOf.SHORT.value)

    def write_ushort(self, value):
        data = struct.pack(Format.UNSIGNED_SHORT.value, value)
        self.write(data, SizeOf.UNSIGNED_SHORT.value)

    def write_int(self, value):
        data = struct.pack(Format.INT.value, value)
        self.write(data, SizeOf.INT.value)

    def write_uint(self, value):
        data = struct.pack(Format.UNSIGNED_INT.value, value)
        self.write(data, SizeOf.UNSIGNED_INT.value)

    def write_long(self, value):
        data = struct.pack(Format.LONG.value, value)
        self.write(data, SizeOf.LONG.value)

    def write_ulong(self, value):
        data = struct.pack(Format.UNSIGNED_LONG.value, value)
        self.write(data, SizeOf.UNSIGNED_LONG.value)

    def write_longlong(self, value):
        data = struct.pack(Format.LONG_LONG.value, value)
        self.write(data, SizeOf.LONG_LONG.value)

    def write_ulonglong(self, value):
        data = struct.pack(Format.UNSIGNED_LONG_LONG.value, value)
        self.write(data, SizeOf.UNSIGNED_LONG_LONG.value)

    def write_float(self, value):
        data = struct.pack(Format.FLOAT.value, value)
        self.write(data, SizeOf.FLOAT.value)

    def write_double(self, value):
        data = struct.pack(Format.DOUBLE.value, value)
        self.write(data, SizeOf.DOUBLE.value)

    """ Read operations """

    def read_char(self):
        data = self.read(SizeOf.CHAR.value)
        return struct.unpack(Format.CHAR.value, data)[0]

    def read_schar(self):
        data = self.read(SizeOf.UNSIGNED_CHAR.value)
        return struct.unpack(Format.UNSIGNED_CHAR.value, data)[0]

    def read_uchar(self):
        data = self.read(SizeOf.UNSIGNED_CHAR.value)
        return struct.unpack(Format.UNSIGNED_CHAR.value, data)[0]

    def read_bool(self):
        data = self.read(SizeOf.BOOL.value)
        return struct.unpack(Format.BOOL.value, data)[0]

    def read_ushort(self):
        data = self.read(SizeOf.UNSIGNED_SHORT.value)
        return struct.unpack(Format.UNSIGNED_SHORT.value, data)[0]

    def read_short(self):
        data = self.read(SizeOf.SHORT.value)
        return struct.unpack(Format.SHORT.value, data)[0]

    def read_int(self):
        data = self.read(SizeOf.INT.value)
        return struct.unpack(Format.INT.value, data)[0]

    def read_uint(self):
        data = self.read(SizeOf.UNSIGNED_INT.value)
        return struct.unpack(Format.UNSIGNED_INT.value, data)[0]

    def read_long(self):
        data = self.read(SizeOf.LONG.value)
        return struct.unpack(Format.LONG.value, data)[0]

    def read_ulong(self):
        data = self.read(SizeOf.UNSIGNED_LONG.value)
        return struct.unpack(Format.UNSIGNED_LONG.value, data)[0]

    def read_longlong(self):
        data = self.read(SizeOf.LONG_LONG.value)
        return struct.unpack(Format.LONG_LONG.value, data)[0]

    def read_float(self):
        data = self.read(SizeOf.FLOAT.value)
        return struct.unpack(Format.FLOAT.value, data)[0]

    def read_double(self):
        data = self.read(SizeOf.DOUBLE.value)
        return struct.unpack(Format.DOUBLE.value, data)[0]

    """ Specific read and write functions """
    def read_string(self):
        string_len = self.read_int()
        data = self.read(string_len)
        return data.decode("utf-8")

    def write_string(self, value):
        raw_value = bytes(value, "utf-8")
        data = raw_value+bytes(1)
        self.write(data, len(raw_value)+1)

    def read_float_array(self, size):
        data = self.read(size * SizeOf.FLOAT.value)
        return struct.unpack(size * Format.FLOAT.value, data)

    def read_int_array(self, size):
        data = self.read(size * SizeOf.INT.value)
        return struct.unpack(size * Format.INT.value, data)

    def read_point2f(self):
        xs = self.read_float_array(2)
        return Point2f(xs[0], xs[1])

    def read_point2i(self):
        xs = self.read_int_array(2)
        return Point2i(xs[0], xs[1])

    def read_point3f(self):
        xs = self.read_float_array(3)
        return Point3f(xs[0], xs[1], xs[2])

    def read_point3i(self):
        xs = self.read_int_array(3)
        return Point3i(xs[0], xs[1], xs[2])

    def read_vec3f(self):
        xs = self.read_float_array(3)
        return Vec3f(xs[0], xs[1], xs[2])

    def read_vec3i(self):
        xs = self.read_int_array(3)
        return Vec3i(xs[0], xs[1], xs[2])

    def read_color3f(self):
        xs = self.read_float_array(4)
        return Color3f(xs[0], xs[1], xs[2], xs[3])

