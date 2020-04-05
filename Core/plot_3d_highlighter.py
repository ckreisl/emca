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


class Highlighter3D(HighlighterBase):

    def __init__(self, figure, axes, callback):
        HighlighterBase.__init__(self, figure, axes, callback)
        self.y = np.array([])
        self.z = np.array([])

    def init_data(self, **kwargs):
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.z = kwargs['z']
        # todo rectangle selector possible?

    def update_all(self, mask):
        pass
