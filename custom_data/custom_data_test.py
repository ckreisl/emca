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

from custom_data.custom_data_base import CustomData
import logging


class CustomDataTest(CustomData):

    """
    CustomDataTest

    Example how to use and add CustomData
    """

    def __init__(self):
        CustomData.__init__(self, 256)

        self._x = 0
        self._y = 0

    def deserialize(self, msg_len, stream):
        """
        Deserialize the data from the socket stream
        :param msg_len:
        :param stream:
        :return:
        """
        self._x = stream.read_int()
        self._y = stream.read_int()

    def create_custom_node(self):
        """
        Add data for visualization in view render data
        add...(description, value)
        :return:
        """
        self.add_data_to_root("x", self._x)
        self.add_data_to_root("y", self._y)
