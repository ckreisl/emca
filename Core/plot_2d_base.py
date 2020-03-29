import matplotlib.pyplot as plt
import numpy as np
from Core.plot_figure_base import FigureBase
from Core.plot_2d_highlighter import Highlighter2D


class ScatterPlot2DBase(FigureBase):

    def __init__(self, callback):
        figure, axes = plt.subplots(figsize=(5, 5), nrows=1)
        FigureBase.__init__(self, figure, axes)
        self.highlighter = Highlighter2D(figure, axes, callback)
        self.figure.tight_layout()

    def plot_2d(self, x, y, init_highlighter=True):
        self.axes.plot(x, y, 'o', color=self.color_dots, picker=5, alpha=self.alpha_dots)
        if init_highlighter:
            self.highlighter.init_dataset(x=np.array(x), s1=np.array(y))
        self.figure.canvas.draw_idle()
