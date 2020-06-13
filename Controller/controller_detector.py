from Detector.detector import Detector
from Core.messages import StateMsg


class ControllerDetector(object):

    def __init__(self, parent, model, view):

        self._controller_main = parent
        self._model = model
        self._view = view

        self._detector = Detector()

        # init detector view with values from detector class
        self._view.view_detector.init_values(self._detector)

    def handle_state_msg(self, tpl):
        msg = tpl[0]
        if msg is StateMsg.DATA_RENDER:
            # check if detector is enabled and run outlier detection
            if self._detector.is_active:
                self.run_detector(self._detector)

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

        self._detector.update_values(m, alpha, k, pre_filter, is_default, is_active)
        # run detector if sample contribution data is available
        if self._model.final_estimate_data.data_loaded:
            self.run_detector(self._detector)

    def run_detector(self, detector):
        """
        Only runs the detector if the checkbox for the detector is active,
        moreover the final estimate data is needed in order to detector outliers
        :param detector:
        :return:
        """
        if detector.is_active:
            if self._model.final_estimate_data.data_loaded:
                data = self._model.final_estimate_data.mean
                detector.run_outlier_detection(data=data)
                self._controller_main.update_path(detector.path_outlier_key_list, False)
            else:
                self._view.view_popup.error_no_final_estimate_data("")
