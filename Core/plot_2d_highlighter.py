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


class Highlighter2D(HighlighterBase):

    def __init__(self, fig, axes, callback):
        HighlighterBase.__init__(self, fig, axes, callback)
        self.s1 = np.array([])

    def init_data(self, **kwargs):
        self.x = kwargs['x']
        self.s1 = kwargs['s1']
        self.add_rectangle_selector(self.axes, self.select_xs1)

    def select_xs1(self, event1, event2):
        mask = self.inside(event1, event2, self.x, self.s1)
        self.callback_send_update_path(self.x[mask], False)

    def update_all(self, mask):
        xs1 = np.column_stack([self.x[mask], self.s1[mask]])
        self.highlighters.set_offsets(xs1)
