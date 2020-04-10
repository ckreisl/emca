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

from Core.highlighter_base import HighlighterBase
import numpy as np
import logging


class RGBHighlighter(HighlighterBase):

    """
        Highlighter
        Handles the item selecting of the plot. Moreover handles User input with Shift+LeftMouseClick to add items
        and "r" to enable / disable a rectangular selection.
    """

    def __init__(self, fig, axes, callback):
        HighlighterBase.__init__(self, fig, axes, callback)
        # default sets
        self.s1 = np.array([])
        self.s2 = np.array([])
        self.s3 = np.array([])

    def init_data(self, **kwargs):
        self.x = kwargs['x']
        self.s1 = kwargs['s1']
        self.s2 = kwargs['s2']
        self.s3 = kwargs['s3']
        self.add_rectangle_selector(self.axes[0], self.select_xs1)
        self.add_rectangle_selector(self.axes[1], self.select_xs2)
        self.add_rectangle_selector(self.axes[2], self.select_xs3)

    def select_xs1(self, event1, event2):
        """
        Send selected items in plot 1
        :param event1:
        :param event2:
        :return:
        """
        mask = self.inside(event1, event2, self.x, self.s1)
        self.callback_send_update_path(self.x[mask], False)

    def select_xs2(self, event1, event2):
        """
        Send selected items in plot 2
        :param event1:
        :param event2:
        :return:
        """
        mask = self.inside(event1, event2, self.x, self.s2)
        self.callback_send_update_path(self.x[mask], False)

    def select_xs3(self, event1, event2):
        """
        Send selected items in plot 3
        :param event1:
        :param event2:
        :return:
        """
        mask = self.inside(event1, event2, self.x, self.s3)
        self.callback_send_update_path(self.x[mask], False)

    def update_all(self, mask):
        """
        Update and highlight the data depending on indicies
        :param mask: boolean array to mark dots
        :return:
        """
        xs1 = np.column_stack([self.x[mask], self.s1[mask]])
        xs2 = np.column_stack([self.x[mask], self.s2[mask]])
        xs3 = np.column_stack([self.x[mask], self.s3[mask]])
        self.highlighters[0].set_offsets(xs1)
        self.highlighters[1].set_offsets(xs2)
        self.highlighters[2].set_offsets(xs3)
