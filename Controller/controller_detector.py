from Core.messages import StateMsg
import logging


class ControllerDetector(object):

    def __init__(self, parent, model, view):

        self._controller_main = parent
        self._model = model
        self._view = view

        # init detector view with values from detector class
        self._view.view_detector.init_values(model.detector)

    def handle_state_msg(self, tpl):
        msg = tpl[0]
        if msg is StateMsg.DATA_RENDER:
            # check if detector is enabled and run outlier detection
            if self._model.detector.is_active:
                self.run_detector()

    def update_and_run_detector(self, m, alpha, k, pre_filter, is_default, is_active):
        """
        Saves all user changes of the detector
        :param m:
        :param alpha:
        :param k:
        :param pre_filter:
        :param is_default:
        :param is_active:
        :return:
        """
        self._model.detector.update_values(m, alpha, k, pre_filter, is_default, is_active)
        # run detector if sample contribution data is available
        if self._model.final_estimate_data.data_loaded:
            self.run_detector()
        else:
            self._view.view_popup.error_no_final_estimate_data("")

    def run_detector(self):
        """
        Only runs the detector if the checkbox for the detector is active,
        moreover the final estimate data is needed in order to detector outliers
        :return:
        """
        detector = self._model.detector
        if detector.is_active:
            data = self._model.final_estimate_data.mean
            path_outliers_indices = detector.run_outlier_detection(data=data)
            if len(path_outliers_indices) > 0:
                self._controller_main.update_path(path_outliers_indices, False)
            else:
                self._view.view_popup.error_outlier_detector_no_outliers_detected("")
        else:
            self._view.view_popup.error_detector_not_enabled("")

