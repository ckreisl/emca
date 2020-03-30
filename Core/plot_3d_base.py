import matplotlib.pyplot as plt
from Core.plot_figure_base import FigureBase
from Core.plot_3d_highlighter import Highlighter3D
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import logging


class ScatterPlot3DBase(FigureBase):

    def __init__(self, callback):
        figure = plt.figure(figsize=(5, 4))
        axes = figure.add_subplot(111, projection='3d')
        FigureBase.__init__(self, figure, axes)
        self.highlighter = Highlighter3D(figure, axes, callback)
        # set axes here - must be created for mouse rotation
        self.axes = Axes3D(self.figure)
        # theme has to be set again
        self.apply_theme('dark')

    def resize_plot(self):
        # overwrite function to avoid figure.tight_layout() call
        pass

    def plot_3d(self, x, y, z, init_highlighter=True):
        self.axes.plot(x, y, z, 'o', color=self.color_dots, picker=5, alpha=self.alpha_dots)
        if init_highlighter:
            self.highlighter.init_data(x=np.array(x), y=np.array(y), z=np.array(y))
        self.figure.canvas.draw_idle()
