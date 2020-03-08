from PyQt5.QtWidgets import QListWidgetItem


class HistListItem(QListWidgetItem):

    def __init__(self, name, list_widget, plot_data, xmin, xmax, plot_canvas, widget_idx):
        QListWidgetItem.__init__(self, name, list_widget)

        self._name = name
        self._plot_data = plot_data
        self._xmin = xmin
        self._xmax = xmax
        self._plot_canvas = plot_canvas
        self._widget_idx = widget_idx

    @property
    def name(self):
        return self._name

    @property
    def plot_data(self):
        return self._plot_data

    @property
    def xmin(self):
        return self._xmin

    @property
    def xmax(self):
        return self._xmax

    @property
    def plot_canvas(self):
        return self._plot_canvas

    @property
    def widget_idx(self):
        return self._widget_idx
