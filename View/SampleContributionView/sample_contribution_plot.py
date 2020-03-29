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

from Core.plot_rgb_base import RGBScatterPlotBase
import logging


class SampleContributionPlot(RGBScatterPlotBase):
    
    """
        SampleContributionPlot
        Visualizes the final estimate data within a plot split in RGB
    """

    def __init__(self, callback=None):
        RGBScatterPlotBase.__init__(self, callback)

        for ax in self.axes:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

    def plot_estimates(self, final_estimate):
        """
        VertexDataPlots the final estimate data
        :param final_estimate: FinalEstimate data
        :return: 
        """
        self.plot_rgb(final_estimate.plot_data_x,
                      final_estimate.red,
                      final_estimate.green,
                      final_estimate.blue)

    def update_path_indices(self, indices):
        """
        Inform the highlighter to highlight and select the given indices
        :param indices: numpy array containing path indices 
        :return: 
        """
        self.highlighter.update(indices)
