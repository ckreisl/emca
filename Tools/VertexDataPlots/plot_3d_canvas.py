from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import logging


class Plot3DCanvas(FigureCanvas):

    def __init__(self, parent=None):
        self._parent = parent
        self._fig = Figure((5, 4), dpi=100)

        FigureCanvas.__init__(self, self._fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self._ax1 = Axes3D(self._fig)
        # self._ax1_highlight, = self._ax1.plot([], [], 'o', color='yellow')

        # self._fig.tight_layout()
        self._cid = self._fig.canvas.mpl_connect('pick_event', self.handle_pick)

    def resize_plot(self):
        #self._fig.tight_layout()
        self._fig.canvas.draw_idle()

    def handle_pick(self, event):
        # todo check if picking and highlighting with idx is possible in 3d plot
        pass

    def clear_plot(self):
        self._ax1.clear()

    def select_vertex(self, tpl):
        # todo check if picking and highlighting with idx is possible in 3d plot
        pass

    def plot(self, name, values, xmin=None, xmax=None):

        x_list = [x[0] for x in values]
        points = [p[1] for p in values]

        y_list = []
        z_list = []

        for p in points:
            tpl = p[0]
            y_list.append(tpl[0])
            z_list.append(tpl[1])

        self._ax1.plot(x_list, y_list, z_list, 'o', picker=5)
        self._ax1.set_title(name)
        self._ax1.set_xlabel('path depth')
        self._ax1.set_ylabel('x')
        self._ax1.set_zlabel('y')
        self._ax1.set_xticks(x_list)
        self._ax1.set_xlim(xmin, xmax)

        #self._fig.tight_layout()
        self._fig.canvas.draw_idle()
