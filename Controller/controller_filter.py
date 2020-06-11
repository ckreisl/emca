from Filter.filter import Filter
from Core.messages import StateMsg
import logging


class ControllerFilter(object):

    def __init__(self, parent, model, view):

        self._controller_main = parent
        self._model = model
        self._view = view

        self._filter = Filter()

    def handle_state_msg(self, tpl):
        msg = tpl[0]
        # run filter
        if msg is StateMsg.DATA_RENDER:
            if self._view.view_filter.is_active():
                render_data = self._model.render_data
                xs = self._filter.apply_filters(render_data)
                self._controller_main.update_path(xs, False)

    def add_filter(self, filter_settings):
        """
        Adds a new filter to the current render data
        :param filter_settings:
        :return:
        """
        self._view.view_filter.add_filter_to_view(filter_settings)
        render_data = self._model.render_data
        xs = self._filter.filter(filter_settings, render_data)
        if xs is None:
            logging.error("Issue with filter ...")
            return
        self._controller_main.update_path(xs, False)

    def apply_filters(self):
        """
        Applies all current active filters to the current render data
        :return:
        """
        render_data = self._model.render_data
        xs = self._filter.apply_filters(render_data)
        self._controller_main.update_path(xs, False)

    def clear_filter(self):
        """
        Clears the filter entries
        :return:
        """
        self._filter.clear_all()
        self._view.view_filter.filterList.clear()

    def delete_filter(self, item):
        """
        Deletes the marked filter and updates the filtered render data.
        Paths which were deleted by the selected filter will be displayed again
        :param item: filter list item
        :return:
        """
        w = self._view.view_filter.filterList.itemWidget(item)
        row = self._view.view_filter.filterList.row(item)
        i = self._view.view_filter.filterList.takeItem(row)
        xs = self._filter.delete_filter(w.get_idx())
        self._controller_main.update_path(xs, False)
        del i
