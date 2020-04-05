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

import matplotlib.pyplot as plt
from Core.plot_figure_base import FigureBase
from Core.plot_rgb_highlighter import RGBHighlighter
import logging


class RGBScatterPlotBase(FigureBase):

    def __init__(self, callback):
        figure, axes = plt.subplots(figsize=(5, 5), nrows=3)
        FigureBase.__init__(self, figure, axes)
        self.highlighter = RGBHighlighter(figure, axes, callback)
        self.init_title()
        self.figure.tight_layout()

    def init_title(self):
        self.figure.axes[0].set_title("Red", color=self.color_title)
        self.figure.axes[1].set_title("Green", color=self.color_title)
        self.figure.axes[2].set_title("Blue", color=self.color_title)

    def plot_rgb(self, x, r, g, b, init_highlighter=True):
        # draw red data
        self.figure.axes[0].plot(x, r, 'o', color='red', picker=5, alpha=self.alpha_dots)
        # draw green data
        self.figure.axes[1].plot(x, g, 'o', color='green', picker=5, alpha=self.alpha_dots)
        # draw blue data
        self.figure.axes[2].plot(x, b, 'o', color='blue', picker=5, alpha=self.alpha_dots)
        # init highlighter with data
        if init_highlighter:
            self.highlighter.init_dataset(x=x, s1=r, s2=g, s3=b)
        # somehow titles gets removed, redraw
        self.init_title()
        self.draw()
