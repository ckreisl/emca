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
import abc


rectprops = dict(
    facecolor='white',
    edgecolor='white',
    alpha=0.2,
    fill=True)


class HighlighterBase(object):

    def __init__(self, figure, axes, callback):
        self.fig = figure
        self.axes = axes
        self.canvas = self.fig.canvas

        self._cid_toggle = self.fig.canvas.mpl_connect('key_press_event', self.key_press_event)
        self._cid_release = self.fig.canvas.mpl_connect('key_release_event', self.key_release_event)
        self._cid_pick = self.fig.canvas.mpl_connect('pick_event', self.pick_event)

        self._rs = []
        self._active = False
        self._hold_shift = False
        self._send_update_path = callback

        self.x = np.array([])
        self.mask = np.array([], dtype=bool)
        self._highlights = None
        self._highlights_color = 'yellow'

    def update_highlighters(self):
        self.delete_highlighter()
        if isinstance(self.axes, np.ndarray):
            self._highlights = [ax.scatter([], [], color=self._highlights_color, zorder=10) for ax in self.axes]
        else:
            self._highlights = self.axes.scatter([], [], color=self._highlights_color, zorder=10)

    def add_rectangle_selector(self, axes, select_func):
        rs = RectangleSelector(axes, select_func, useblit=True, rectprops=rectprops)
        self._rs.append(rs)

    def clear_rectangle_selectors(self):
        self._rs.clear()

    def delete_highlighter(self):
        del self._highlights
        self._highlights = None

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

    def inside(self, event1, event2, x, y):
        x0, x1 = sorted([event1.xdata, event2.xdata])
        y0, y1 = sorted([event1.ydata, event2.ydata])
        return (x > x0) & (x < x1) & (y > y0) & (y < y1)

    def update(self, indices):
        mask = np.isin(self.x, indices)
        self.update_all(mask)
        self.canvas.draw_idle()

    def init_dataset(self, **kwargs):
        self.clear_rectangle_selectors()
        self.init_data(**kwargs)
        self.mask = np.zeros(self.x.shape, dtype=bool)
        self.update_highlighters()
        self.enable_rectangle_selector(self._active)

    @abc.abstractmethod
    def update_all(self, mask):
        pass

    @abc.abstractmethod
    def init_data(self, **kwargs):
        pass








