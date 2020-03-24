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

from View.SampleContributionView.highlighter import Highlighter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy

white = "#eff0f1"
params = {"ytick.color": white,
          "xtick.color": white,
          "axes.labelcolor": white,
          "axes.edgecolor": white}
plt.rcParams.update(params)


class RGBScatterPlot(FigureCanvas):
    
    """
        RGBScatterPlot
        Visualizes the final estimate data within a plot split in RGB
    """

    def __init__(self, callback=None):
        self._fig, self._axes = plt.subplots(figsize=(5, 5), nrows=3)

        # set color equal to qt gui
        # self._RGBA = '#f0f0f0'
        # RGBA dark theme
        self._RGBA = '#31363b'
        self._fig.patch.set_facecolor(self._RGBA)

        # plot facecolor dark theme
        plot_facecolor = '#232629'
        for ax in self._axes:
            ax.set_facecolor(plot_facecolor)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        self._alpha = 0.7

        FigureCanvas.__init__(self, self._fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self._highlighter = Highlighter(self._fig, self._axes, callback)
        self.init_title()
        self._fig.tight_layout()

    def init_title(self):
        """
        Init the title of the plots
        :return: 
        """
        self._axes[0].set_title("Red", color=white)
        self._axes[1].set_title("Green", color=white)
        self._axes[2].set_title("Blue", color=white)

    def clear_plots(self):
        """
        Clears the plots
        :return: 
        """
        for axes in self._axes:
            axes.clear()

    def plot_estimates(self, final_estimate):
        """
        VertexDataPlots the final estimate data
        :param final_estimate: FinalEstimate data
        :return: 
        """
        
        # draw red data
        self._axes[0].plot(final_estimate.plot_data_x,
                           final_estimate.red, 'o', color='red', picker=5, alpha=self._alpha)
        # draw green data
        self._axes[1].plot(final_estimate.plot_data_x,
                           final_estimate.green, 'o', color='green', picker=5, alpha=self._alpha)
        # draw blue data
        self._axes[2].plot(final_estimate.plot_data_x,
                           final_estimate.blue, 'o', color='blue', picker=5, alpha=self._alpha)

        # init highlighter
        self._highlighter.init_dataset(x=final_estimate.plot_data_x,
                                       s1=final_estimate.red,
                                       s2=final_estimate.green,
                                       s3=final_estimate.blue)

        self.init_title()
        self.draw()

    def update_path_indices(self, indices):
        """
        Inform the highlighter to highlight and select the given indices
        :param indices: numpy array containing path indices 
        :return: 
        """
        self._highlighter.update(indices)
