from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.figure import Figure
import numpy as np


class PlotColorCanvas(FigureCanvas):

    def __init__(self, parent=None):
        self._parent = parent
        self._fig = Figure((5, 5), dpi=100)

        FigureCanvas.__init__(self, self._fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self._ax1 = self._fig.add_subplot(311)
        self._ax2 = self._fig.add_subplot(312)
        self._ax3 = self._fig.add_subplot(313)
        #self._ax4 = self._fig.add_subplot(414)

        self._ax1.set_title("Red")
        self._ax2.set_title("Green")
        self._ax3.set_title("Blue")
        #self._ax4.set_title("Alpha")

        self._ax1_highlight, = self._ax1.plot([], [], 'o', color='yellow')
        self._ax2_highlight, = self._ax2.plot([], [], 'o', color='yellow')
        self._ax3_highlight, = self._ax3.plot([], [], 'o', color='yellow')
        #self._ax4_highlight, = self._ax4.plot([], [], 'o', color='yellow')

        self._fig.tight_layout()
        self._cid = self._fig.canvas.mpl_connect('pick_event', self.handle_pick)

    def resize_plot(self):
        self._fig.tight_layout()
        self._fig.canvas.draw_idle()

    def handle_pick(self, event):
        ind = event.ind
        line_ax1 = self._ax1.lines[0]
        x_data_ax1 = line_ax1.get_xdata()

        path_idx = self._parent.current_path_index()
        x_data_ax1 = line_ax1.get_xdata()

        tpl = (path_idx, x_data_ax1[ind[0]])
        self._parent.send_select_vertex(tpl)

    def clear_plot(self):
        self._ax1.clear()
        self._ax2.clear()
        self._ax3.clear()
        #self._ax4.clear()

    def select_vertex(self, tpl):
        line_ax1 = self._ax1.lines[0]
        line_ax2 = self._ax2.lines[0]
        line_ax3 = self._ax3.lines[0]
        #line_ax4 = self._ax4.lines[0]
        y_data_ax1 = line_ax1.get_ydata()
        y_data_ax2 = line_ax2.get_ydata()
        y_data_ax3 = line_ax3.get_ydata()
        #y_data_ax4 = line_ax4.get_ydata()

        x_data_ax1 = line_ax1.get_xdata()
        idx = np.where(x_data_ax1 == tpl[1])[0]

        self._ax1_highlight.set_data(x_data_ax1[idx], y_data_ax1[idx])
        self._ax2_highlight.set_data(x_data_ax1[idx], y_data_ax2[idx])
        self._ax3_highlight.set_data(x_data_ax1[idx], y_data_ax3[idx])
        #self._ax4_highlight.set_data(x_data_ax1[idx], y_data_ax4[idx])
        self._fig.canvas.draw_idle()

    def plot(self, name, values, xmin=None, xmax=None):

        x_list = [x[0] for x in values]
        points = [p[1] for p in values]

        red_list = []
        green_list = []
        blue_list = []
        #alpha_list = []

        for p in points:
            tpl = p[0]
            red_list.append(tpl[0])
            green_list.append(tpl[1])
            blue_list.append(tpl[2])
            #alpha_list.append(tpl[3])

        self._ax1.set_title("Red")
        self._ax2.set_title("Green")
        self._ax3.set_title("Blue")
        #self._ax4.set_title("Alpha")

        self._ax1.plot(x_list, red_list, 'ro', picker=5)
        self._ax1.set_xlabel('path depth')
        self._ax2.plot(x_list, green_list, 'go', picker=5)
        self._ax2.set_xlabel('path depth')
        self._ax3.plot(x_list, blue_list, 'bo', picker=5)
        self._ax3.set_xlabel('path depth')
        #self._ax4.plot(x_list, alpha_list, 'o', color='gray', picker=5)
        #self._ax4.set_xlabel('path depth')

        self._ax1.set_xticks(x_list)
        self._ax2.set_xticks(x_list)
        self._ax3.set_xticks(x_list)
        #self._ax4.set_xticks(x_list)

        self._ax1.set_xlim(xmin, xmax)
        self._ax2.set_xlim(xmin, xmax)
        self._ax3.set_xlim(xmin, xmax)
        #self._ax4.set_xlim(xmin, xmax)

        self._ax1_highlight, = self._ax1.plot([], [], 'o', color='yellow')
        self._ax2_highlight, = self._ax2.plot([], [], 'o', color='yellow')
        self._ax3_highlight, = self._ax3.plot([], [], 'o', color='yellow')
        #self._ax4_highlight, = self._ax4.plot([], [], 'o', color='yellow')

        self._fig.tight_layout()
        self._fig.canvas.draw_idle()
