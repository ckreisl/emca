from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.figure import Figure
import numpy as np
import logging


class Plot2DCanvas(FigureCanvas):

    def __init__(self, parent=None):
        self._parent = parent
        self._fig = Figure((5, 4), dpi=100)

        self._ax1 = self._fig.add_subplot(111)

        FigureCanvas.__init__(self, self._fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self._ax1_highlight, = self._ax1.plot([], [], 'o', color='yellow')

        self._fig.tight_layout()
        self._cid = self._fig.canvas.mpl_connect('pick_event', self.handle_pick)

    def resize_plot(self):
        self._fig.tight_layout()
        self._fig.canvas.draw_idle()

    def handle_pick(self, event):
        ind = event.ind
        line_ax1 = self._ax1.lines[0]

        path_idx = self._parent.current_path_index()
        x_data_ax1 = line_ax1.get_xdata()

        tpl = (path_idx, x_data_ax1[ind[0]])
        self._parent.send_select_vertex(tpl)

    def clear_plot(self):
        self._ax1.clear()

    def select_vertex(self, tpl):
        try:
            line_ax1 = self._ax1.lines[0]
        except IndexError as e:
            logging.error("No data available: {}".format(e))
            return None
        x_data_ax1 = line_ax1.get_xdata()
        y_data_ax1 = line_ax1.get_ydata()

        idx = np.where(x_data_ax1 == tpl[1])[0]

        self._ax1_highlight.set_data(x_data_ax1[idx], y_data_ax1[idx])
        self._fig.canvas.draw_idle()

    def plot(self, name, values, xmin=None, xmax=None):

        x_list = [x[0] for x in values]
        y_list = [y[1] for y in values]

        self._ax1.plot(x_list, y_list, 'bo', picker=5)
        self._ax1.set_xlim(xmin, xmax)
        self._ax1.set_xticks(x_list)
        self._ax1.set_title(name)
        self._ax1.set_ylabel(name)
        self._ax1.set_xlabel('path depth')

        self._ax1_highlight, = self._ax1.plot([], [], 'o', color='yellow')

        self._fig.tight_layout()
        self._fig.canvas.draw_idle()
