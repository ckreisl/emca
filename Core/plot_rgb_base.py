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
