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

from Core.highlighter_base import HighlighterBase
import numpy as np
import logging


class Highlighter(HighlighterBase):

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
        self._send_update_path(self.x[mask], False)

    def select_xs2(self, event1, event2):
        """
        Send selected items in plot 2
        :param event1:
        :param event2:
        :return:
        """
        mask = self.inside(event1, event2, self.x, self.s2)
        self._send_update_path(self.x[mask], False)

    def select_xs3(self, event1, event2):
        """
        Send selected items in plot 3
        :param event1:
        :param event2:
        :return:
        """
        mask = self.inside(event1, event2, self.x, self.s3)
        self._send_update_path(self.x[mask], False)

    def update_all(self, mask):
        """
        Update and highlight the data depending on indicies
        :param mask: boolean array to mark dots
        :return:
        """
        xs1 = np.column_stack([self.x[mask], self.s1[mask]])
        self._highlights[0].set_offsets(xs1)
        xs2 = np.column_stack([self.x[mask], self.s2[mask]])
        self._highlights[1].set_offsets(xs2)
        xs3 = np.column_stack([self.x[mask], self.s3[mask]])
        self._highlights[2].set_offsets(xs3)
