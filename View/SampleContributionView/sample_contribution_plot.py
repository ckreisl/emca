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
