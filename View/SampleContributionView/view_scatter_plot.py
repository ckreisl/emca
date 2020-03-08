from View.SampleContributionView.scatter_plot import RGBScatterPlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolBar
import logging


class ViewScatterPlot(QWidget):

    """
        ViewScatterPlot
        Handles the plot view of the final estimate data per path.
        A matplotlib plot is embedded within a QWidget for visualization
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self._controller = None
        # matplotlib plot embedded within a QWidget
        self._static_canvas = RGBScatterPlot(callback=self.send_update_path)
        # need the following two lines to allow 'key_press_event' for matplotlib VertexDataPlots
        self._static_canvas.setFocusPolicy(Qt.ClickFocus)
        self._static_canvas.setFocus()

        # add matplotlib navigation toolbar
        layout = QVBoxLayout(self)
        layout.addWidget(self._static_canvas)
        layout.addWidget(NavigationToolBar(self._static_canvas, self))

    def set_controller(self, controller):
        """
        Sets the connection to the controller
        :param controller: Controller
        :return:
        """
        self._controller = controller

    def plot_final_estimate(self, final_estimate):
        """
        VertexDataPlots the final estimate data from the model
        :param final_estimate: Final estimate data from model
        :return:
        """
        self._static_canvas.clear_plots()
        if final_estimate.is_valid():
            self._static_canvas.plot_estimates(final_estimate)

    def update_path_indices(self, indices):
        """
        Inform the plot to mark the given indices
        :param indices: numpy array of path indices
        :return:
        """
        self._static_canvas.update_path_indices(indices)

    def send_update_path(self, indices, add_index):
        """
        Inform the controller about selected points from the plot,
        depending on add_index the indices are added to the current selected ones
        :param indices: numpy array of path indices
        :param add_index: boolean
        :return:
        """
        self._controller.update_path(indices, add_index)

