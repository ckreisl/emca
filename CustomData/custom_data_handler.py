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

import CustomData
import logging


class CustomDataHandler(object):

    """
        CustomDataHandler

        Handles all CustomData types.
        Loads and inits the classes which are imported and defined in CustomData/__init__.py
    """

    def __init__(self):

        # custom data dictionary {custom_data_id : custom_data, ...}
        self._custom_data = {}

        # loads and initialises the custom data
        for custom_data in [(name, cls()) for name, cls in CustomData.__dict__.items() if isinstance(cls, type)]:
            self._custom_data[custom_data[1].id] = custom_data[1]

    def get_custom_data_by_id(self, unique_id):
        """
        Returns the corresponding custom data to the given unique_id.
        If no data is defined None is returned
        :param unique_id: custom_data_id
        :return: returns None if no custom data is found with the given id
        """
        return self._custom_data.get(unique_id, None)
