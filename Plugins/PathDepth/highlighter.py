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

from matplotlib.widgets import RectangleSelector
import numpy as np
import logging


class Highlighter(object):

    def __init__(self, fig, axes, callback):
        self.fig = fig
        self.axes = axes
        self.canvas = axes.figure.canvas
        self._cid_toggle = self.fig.canvas.mpl_connect('key_press_event', self.key_press_event)
        self._cid_release = self.fig.canvas.mpl_connect('key_release_event', self.key_release_event)
        self._cid_pick = self.fig.canvas.mpl_connect('pick_event', self.pick_event)
        self._rs = []
        self._active = False
        self._hold_shift = False
        self._send_update_path = callback
        # default sets
        self.x = np.array([])
        self.s1 = np.array([])
        self.mask = np.array([], dtype=bool)
        self._highlights = []

    def init_dataset(self, x, s1):
        self.x = x
        self.s1 = s1
        self.mask = np.zeros(x.shape, dtype=bool)
        self._highlights = self.axes.scatter([], [], color='yellow', zorder=10)
        self._rs.clear()
        self._rs.append(RectangleSelector(self.axes, self.select_xs1, useblit=True))
        self.enable_rectangle_selector(self._active)

    def pick_event(self, event):
        ind = event.ind
        if self._hold_shift:
            self._send_update_path(np.array([ind[0]]), True)
        else:
            self._send_update_path(np.array([ind[0]]), False)

    def key_press_event(self, event):
        if event.key in ['R', 'r']:
            logging.info("Pressed key R")
            self._active = not self._active
            self.enable_rectangle_selector(self._active)
            self.enable_pick_event_selector(not self._active)
        if event.key == 'shift':
            logging.info("Shift press")
            self._hold_shift = True

    def key_release_event(self, event):
        if event.key == 'shift':
            logging.info("Shift release")
            self._hold_shift = False

    def enable_rectangle_selector(self, enable):
        for rs in self._rs:
            rs.set_active(enable)

    def enable_pick_event_selector(self, enable):
        if enable:
            logging.info("connect pick event")
            self._cid_pick = self.fig.canvas.mpl_connect('pick_event', self.pick_event)
        else:
            logging.info("disconnect pick event")
            self.fig.canvas.mpl_disconnect(self._cid_pick)

    def select_xs1(self, event1, event2):
        mask = self.inside(event1, event2, self.x, self.s1)
        self._send_update_path(self.x[mask], False)

    def inside(self, event1, event2, x, y):
        x0, x1 = sorted([event1.xdata, event2.xdata])
        y0, y1 = sorted([event1.ydata, event2.ydata])
        return (x > x0) & (x < x1) & (y > y0) & (y < y1)

    def update(self, indices):
        mask = np.isin(self.x, indices)

        xs1 = np.column_stack([self.x[mask], self.s1[mask]])
        self._highlights.set_offsets(xs1)

        self.canvas.draw_idle()
