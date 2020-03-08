from matplotlib.widgets import RectangleSelector
import numpy as np
import logging


class Highlighter(object):

    """
        Highlighter
        Handles the item selecting of the plot. Moreover handles User input with Shift+LeftMouseClick to add items
        and "r" to enable / disable a rectangular selection.
    """

    def __init__(self, fig, axes, callback):
        self.fig = fig
        self.axes = axes
        self.canvas = axes[0].figure.canvas
        self._cid_toggle = self.fig.canvas.mpl_connect('key_press_event', self.key_press_event)
        self._cid_release = self.fig.canvas.mpl_connect('key_release_event', self.key_release_event)
        self._cid_pick = self.fig.canvas.mpl_connect('pick_event', self.pick_event)
        self._rs = []
        self._active = False
        self._hold_shift = False
        self._send_update_path = callback
        # default sets
        self.x = np.array([])
        self.s1 = np.array([])
        self.s2 = np.array([])
        self.s3 = np.array([])
        self.mask = np.array([], dtype=bool)
        self._highlights = []

    def init_dataset(self, x, s1, s2, s3):
        """
        Initialise the dataset.
        :param x: x-axis data (same everywhere)
        :param s1: y-data plot 1
        :param s2: y-data plot 2
        :param s3: y-data plot 3
        :return:
        """
        self.x = x
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.mask = np.zeros(x.shape, dtype=bool)
        self._highlights = [ax.scatter([], [], color='yellow', zorder=10) for ax in self.axes]
        self._rs.clear()
        self._rs.append(RectangleSelector(self.axes[0], self.select_xs1, useblit=True))
        self._rs.append(RectangleSelector(self.axes[1], self.select_xs2, useblit=True))
        self._rs.append(RectangleSelector(self.axes[2], self.select_xs3, useblit=True))
        self.enable_rectangle_selector(self._active)

    def pick_event(self, event):
        """
        Handle a single pick event, checks if shift is pressed to add the next selected item to the current ones.
        Sends an inform message to the controller about selected items via callback.
        :param event:
        :return:
        """
        ind = event.ind
        if self._hold_shift:
            self._send_update_path(np.array([ind[0]]), True)
        else:
            self._send_update_path(np.array([ind[0]]), False)

    def key_press_event(self, event):
        """
        Checks if a key is pressed, Shift for adding single values or "r" for enabling the rectangular selector.
        :param event:
        :return:
        """
        if event.key in ['R', 'r']:
            logging.info("Pressed key R")
            self._active = not self._active
            self.enable_rectangle_selector(self._active)
            self.enable_pick_event_selector(not self._active)
        if event.key == 'shift':
            logging.info("Shift press")
            self._hold_shift = True

    def key_release_event(self, event):
        """
        Handles the key release event
        :param event:
        :return:
        """
        if event.key == 'shift':
            logging.info("Shift release")
            self._hold_shift = False

    def enable_rectangle_selector(self, enable):
        """
        Enables the rectangular selector
        :param enable: boolean
        :return:
        """
        for rs in self._rs:
            rs.set_active(enable)

    def enable_pick_event_selector(self, enable):
        """
        Enables or disables the single pick event depending on enable
        :param enable: boolean
        :return:
        """
        if enable:
            logging.info("connect pick event")
            self._cid_pick = self.fig.canvas.mpl_connect('pick_event', self.pick_event)
        else:
            logging.info("disconnect pick event")
            self.fig.canvas.mpl_disconnect(self._cid_pick)

    def select_xs1(self, event1, event2):
        """
        Send selected items in plot 1
        :param event1:
        :param event2:
        :return:
        """
        mask = self.inside(event1, event2, self.x, self.s1)
        self._send_update_path(self.x[mask], False)

    def select_xs2(self, event1, event2):
        """
        Send selected items in plot 2
        :param event1:
        :param event2:
        :return:
        """
        mask = self.inside(event1, event2, self.x, self.s2)
        self._send_update_path(self.x[mask], False)

    def select_xs3(self, event1, event2):
        """
        Send selected items in plot 3
        :param event1:
        :param event2:
        :return:
        """
        mask = self.inside(event1, event2, self.x, self.s3)
        self._send_update_path(self.x[mask], False)

    def inside(self, event1, event2, x, y):
        """
        Check if data is within the selected set
        :param event1:
        :param event2:
        :param x:
        :param y:
        :return:
        """
        x0, x1 = sorted([event1.xdata, event2.xdata])
        y0, y1 = sorted([event1.ydata, event2.ydata])
        return (x > x0) & (x < x1) & (y > y0) & (y < y1)

    def update(self, indices):
        """
        Update and highlight the data depending on indicies
        :param indices: numpy array with path indices
        :return:
        """
        mask = np.isin(self.x, indices)

        xs1 = np.column_stack([self.x[mask], self.s1[mask]])
        self._highlights[0].set_offsets(xs1)

        xs2 = np.column_stack([self.x[mask], self.s2[mask]])
        self._highlights[1].set_offsets(xs2)

        xs3 = np.column_stack([self.x[mask], self.s3[mask]])
        self._highlights[2].set_offsets(xs3)

        self.canvas.draw_idle()
