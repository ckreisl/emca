from Tools.PathDepth.highlighter import Highlighter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
import matplotlib.pyplot as plt
import numpy as np
import logging


class PlotPathDepth(FigureCanvas):

    def __init__(self, callback=None):
        self._callback = callback
        self._fig, self._axes = plt.subplots(figsize=(5, 5), nrows=1)

        FigureCanvas.__init__(self, self._fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self._highlighter = Highlighter(self._fig, self._axes, callback)
        self._fig.tight_layout()

    def resize_plot(self):
        self._fig.tight_layout()
        self._fig.canvas.draw_idle()

    def select_path(self, index):
        self._highlighter.update(np.array([index]))

    def mark_values(self, indices):
        self._highlighter.update(indices)

    def clear_plot(self):
        self._axes.clear()

    def plot(self, x_list, y_list):
        self._axes.plot(x_list, y_list, 'bo', picker=5)
        self._axes.set_ylabel('path depth')
        self._axes.set_xlabel('paths')
        self._highlighter.init_dataset(np.array(x_list),
                                       np.array(y_list))
        self._fig.canvas.draw_idle()
        self._fig.tight_layout()
