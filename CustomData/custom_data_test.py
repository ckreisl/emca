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

from CustomData.custom_data_base import CustomData
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
