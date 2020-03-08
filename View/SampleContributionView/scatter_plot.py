from View.SampleContributionView.highlighter import Highlighter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy


class RGBScatterPlot(FigureCanvas):
    
    """
        RGBScatterPlot
        Visualizes the final estimate data within a plot split in RGB
    """

    def __init__(self, callback=None):
        self._fig, self._axes = plt.subplots(figsize=(5, 5), nrows=3)

        # set color equal to qt gui
        self._RGBA = '#f0f0f0'
        self._fig.patch.set_facecolor(self._RGBA)

        FigureCanvas.__init__(self, self._fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self._highlighter = Highlighter(self._fig, self._axes, callback)
        self.init_title()
        self._fig.tight_layout()

    def init_title(self):
        """
        Init the title of the plots
        :return: 
        """
        self._axes[0].set_title("Red")
        self._axes[1].set_title("Green")
        self._axes[2].set_title("Blue")

    def clear_plots(self):
        """
        Clears the plots
        :return: 
        """
        for axes in self._axes:
            axes.clear()

    def plot_estimates(self, final_estimate):
        """
        VertexDataPlots the final estimate data
        :param final_estimate: FinalEstimate data
        :return: 
        """
        
        # draw red data
        self._axes[0].plot(final_estimate.plot_data_x,
                           final_estimate.red, 'o', color='red', picker=5)
        # draw green data
        self._axes[1].plot(final_estimate.plot_data_x,
                           final_estimate.green, 'o', color='green', picker=5)
        # draw blue data
        self._axes[2].plot(final_estimate.plot_data_x,
                           final_estimate.blue, 'o', color='blue', picker=5)

        # init highlighter
        self._highlighter.init_dataset(final_estimate.plot_data_x,
                                       final_estimate.red,
                                       final_estimate.green,
                                       final_estimate.blue)

        self.init_title()
        self.draw()

    def update_path_indices(self, indices):
        """
        Inform the highlighter to highlight and select the given indices
        :param indices: numpy array containing path indices 
        :return: 
        """
        self._highlighter.update(indices)
