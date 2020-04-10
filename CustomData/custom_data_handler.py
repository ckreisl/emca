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
