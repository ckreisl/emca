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

from custom_data.custom_data_handler import CustomDataHandler
import logging


class UserData(object):

    """
        UserData
        Handles general data types which can be added by the user during the path tracing algorithm,
        in order to debug the system.
        Supported data types boolean, float, double, integer, point2i, point2f, point3i, point3f, color3f and vectors
    """

    def __init__(self):
        # handle default data types
        self._dict_bool = {}
        self._dict_float = {}
        self._dict_double = {}
        self._dict_int = {}
        self._dict_point2i = {}
        self._dict_point2f = {}
        self._dict_point3i = {}
        self._dict_point3f = {}
        self._dict_color3f = {}
        self._dict_string = {}
        self._data = []
        # handle custom data
        self._dict_custom_data = {}
        self._custom_data_handler = CustomDataHandler()

    def deserialize(self, stream):
        """
        Deserialize UserData class from a socket stream
        :param stream:
        :return:
        """
        self.clear()
        self._dict_bool = self._deserialize_bool(stream)
        self._dict_float = self._deserialize_float(stream)
        self._dict_double = self._deserialize_double(stream)
        self._dict_int = self._deserialize_int(stream)
        self._dict_point2i = self._deserialize_point2i(stream)
        self._dict_point2f = self._deserialize_point2f(stream)
        self._dict_point3i = self._deserialize_point3i(stream)
        self._dict_point3f = self._deserialize_point3f(stream)
        self._dict_color3f = self._deserialize_color3f(stream)
        self._dict_string = self._deserialize_string(stream)
        self._dict_custom_data = self._deserialize_custom_data(stream)
        self.init_data_list()

    def init_data_list(self):
        """
        Creates a list of containing UserData dicts which are not zero
        :return:
        """
        if len(self._dict_bool) > 0:
            self._data.append(self._dict_bool)
        if len(self._dict_float) > 0:
            self._data.append(self._dict_float)
        if len(self._dict_double) > 0:
            self._data.append(self._dict_double)
        if len(self._dict_int) > 0:
            self._data.append(self._dict_int)
        if len(self._dict_point2i) > 0:
            self._data.append(self._dict_point2i)
        if len(self._dict_point2f) > 0:
            self._data.append(self._dict_point2f)
        if len(self._dict_point3i) > 0:
            self._data.append(self._dict_point3i)
        if len(self._dict_point3f) > 0:
            self._data.append(self._dict_point3f)
        if len(self._dict_color3f) > 0:
            self._data.append(self._dict_color3f)
        if len(self._dict_string) > 0:
            self._data.append(self._dict_string)

    @property
    def data_list(self):
        """
        Returns a list containing data dicts with set information
        :return: list
        """
        return self._data

    @property
    def dict_bool(self):
        """
        Returns the bool dict
        :return: dict {name : value, ...}
        """
        return self._dict_bool

    @property
    def dict_float(self):
        """
        Returns the float dict
        :return: dict{name : value, ...}
        """
        return self._dict_float

    @property
    def dict_double(self):
        """
        Returns the double dict
        :return: dict{name : value, ...}
        """
        return self._dict_double

    @property
    def dict_int(self):
        """
        Returns the int dict
        :return: dict{name : value, ...}
        """
        return self._dict_int

    @property
    def dict_point2i(self):
        """
        Returns the point2i dict
        :return: dict{name : value, ...}
        """
        return self._dict_point2i

    @property
    def dict_point2f(self):
        """
        Returns the point2f dict
        :return: dict{name : value, ...}
        """
        return self._dict_point2f

    @property
    def dict_point3i(self):
        """
        Returns the point3 dict
        :return: dict{name : value, ...}
        """
        return self._dict_point3i

    @property
    def dict_point3f(self):
        """
        Returns the point3f dict
        :return: dict{name : value, ...}
        """
        return self._dict_point3f

    @property
    def dict_color3f(self):
        """
        Returns the color3f dict
        :return:
        """
        return self._dict_color3f

    @property
    def dict_string(self):
        """
        Returns the string dict
        :return:
        """
        return self._dict_string

    @property
    def dict_custom_data(self):
        """
        Returns the custom data dict
        :return: dict{custom_data_index : CustomData, ...}
        """
        return self._dict_custom_data

    def clear(self):
        """
        Clears all data sets
        :return:
        """
        self._dict_bool.clear()
        self._dict_float.clear()
        self._dict_double.clear()
        self._dict_int.clear()
        self._dict_point2i.clear()
        self._dict_point2f.clear()
        self._dict_point3i.clear()
        self._dict_point3f.clear()
        self._dict_color3f.clear()
        self._dict_string.clear()
        self._dict_custom_data.clear()
        self._data.clear()

    @staticmethod
    def _deserialize_bool(stream):
        """
        Deserialize user added information from the socket stream
        :param stream:
        :return:
        """
        dict_bool = {}
        for i in range(0, stream.read_uint()):
            key = stream.read_string()
            data = []
            for j in range(0, stream.read_uint()):
                data.append(stream.read_bool())
            dict_bool[key] = data
        return dict_bool

    @staticmethod
    def _deserialize_float(stream):
        """
        Deserialize user added information from the socket stream
        :param stream:
        :return:
        """
        dict_float = {}
        for i in range(0, stream.read_uint()):
            key = stream.read_string()
            data = []
            for j in range(0, stream.read_uint()):
                data.append(stream.read_float())
            dict_float[key] = data
        return dict_float

    @staticmethod
    def _deserialize_double(stream):
        """
        Deserialize user added information from the socket stream
        :param stream:
        :return:
        """
        dict_double = {}
        for i in range(0, stream.read_uint()):
            key = stream.read_string()
            data = []
            for j in range(0, stream.read_uint()):
                data.append(stream.read_double())
            dict_double[key] = data
        return dict_double

    @staticmethod
    def _deserialize_int(stream):
        """
        Deserialize user added information from the socket stream
        :param stream:
        :return:
        """
        dict_int = {}
        for i in range(0, stream.read_uint()):
            key = stream.read_string()
            data = []
            for j in range(0, stream.read_uint()):
                data.append(stream.read_int())
            dict_int[key] = data
        return dict_int

    @staticmethod
    def _deserialize_point2i(stream):
        """
        Deserialize user added information from the socket stream
        :param stream:
        :return:
        """
        dict_point2i = {}
        for i in range(0, stream.read_uint()):
            key = stream.read_string()
            data = []
            for j in range(0, stream.read_uint()):
                data.append(stream.read_point2i())
            dict_point2i[key] = data
        return dict_point2i

    @staticmethod
    def _deserialize_point2f(stream):
        """
        Deserialize user added information from the socket stream
        :param stream:
        :return:
        """
        dict_point2f = {}
        for i in range(0, stream.read_uint()):
            key = stream.read_string()
            data = []
            for j in range(0, stream.read_uint()):
                data.append(stream.read_point2f())
            dict_point2f[key] = data
        return dict_point2f

    @staticmethod
    def _deserialize_point3i(stream):
        """
        Deserialize user added information from the socket stream
        :param stream:
        :return:
        """
        dict_point3i = {}
        for i in range(0, stream.read_uint()):
            key = stream.read_string()
            data = []
            for j in range(0, stream.read_uint()):
                data.append(stream.read_point3i())
            dict_point3i[key] = data
        return dict_point3i

    @staticmethod
    def _deserialize_point3f(stream):
        """
        Deserialize user added information from the socket stream
        :param stream:
        :return:
        """
        dict_point3f = {}
        for i in range(0, stream.read_uint()):
            key = stream.read_string()
            data = []
            for j in range(0, stream.read_uint()):
                data.append(stream.read_point3f())
            dict_point3f[key] = data
        return dict_point3f

    @staticmethod
    def _deserialize_color3f(stream):
        """
        Deserialize user added information from the socket stream
        :param stream:
        :return:
        """
        dict_color3f = {}
        for i in range(0, stream.read_uint()):
            key = stream.read_string()
            data = []
            for j in range(0, stream.read_uint()):
                data.append(stream.read_color3f())
            dict_color3f[key] = data
        return dict_color3f

    @staticmethod
    def _deserialize_string(stream):
        """
        Deserialize user added information from the socket stream
        :param stream:
        :return:
        """
        dict_string = {}
        for i in range(0, stream.read_uint()):
            key = stream.read_string()
            data = []
            for j in range(0, stream.read_uint()):
                data.append(stream.read_string())
            dict_string[key] = data
        return dict_string

    def _deserialize_custom_data(self, stream):
        """
        Deserialize CustomData from the socket stream.
        If the header index does not match andy custom data the package is rejected,
        otherwise the specific custom data class will deserialize the data from the socket stream.
        :param stream:
        :return: dict{custom_data_index : CustomData, ...}
        """
        dict_custom_data = {}
        for i in range(0, stream.read_uint()):
            key = stream.read_short()
            name = stream.read_string()
            msg_len = stream.read_uint()
            custom_data = self._custom_data_handler.get_custom_data_by_id(key)
            if custom_data:
                # deserialize custom data
                custom_data.name = name
                custom_data.deserialize(msg_len, stream)
                dict_custom_data[key] = custom_data
            else:
                # clean stream
                stream.read(msg_len)
        return dict_custom_data
