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
