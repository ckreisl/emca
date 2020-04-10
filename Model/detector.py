"""
    MIT License

    Copyright (c) 2020 Christoph Kreisl

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import six.moves as smo
import numpy as np
import logging
import time


class Detector(object):

    """
        Detector
        Detects outliers based on two algorithms
        1. Mean squared error with Standard deviation
        2. Generalized ESD Rosner
        Therefore the Final Estimate data set is used to identify paths with high contribution
    """

    def __init__(self):
        # enable or disable filtering by detector
        self._active = False

        # run default or esd outlier detection
        self._default = True

        # esd outlier settings
        self._k = 1
        self._alpha = 0.05
        self._filter = 1.0

        # default outlier settings
        self._m = 2

        # path outlier key list
        self._path_outlier_key_list = np.array([], dtype=np.int32)

        # list of outliers as tupel (path_key, vertex_key)
        self._outlier_tpls_list = []

    def is_default_active(self):
        return self._default

    def set_default_active(self, enable):
        self._default = enable

    @property
    def is_active(self):
        return self._active

    @is_active.setter
    def is_active(self, enable):
        self._active = enable

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, new_k):
        self._k = new_k

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, new_alpha):
        self._alpha = new_alpha

    @property
    def pre_filter(self):
        return self._filter

    @pre_filter.setter
    def pre_filter(self, new_filter):
        self._filter = new_filter

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, new_m):
        self._m = new_m

    def update_values(self, m, alpha, k, pre_filter, is_default, is_active):
        """
        Updates all values of the detector class
        :param m:
        :param alpha:
        :param k:
        :param pre_filter:
        :param is_default:
        :param is_active:
        :return:
        """
        self._m = m
        self._alpha = alpha
        self._k = k
        self._filter = pre_filter
        self._default = is_default
        self._active = is_active

    @property
    def path_outlier_key_list(self):
        return self._path_outlier_key_list

    @property
    def outliers_tpls_list(self):
        return self._outlier_tpls_list

    def soft_detection(self, path_key_list, render_data):
        """
        Soft detection, finds the first path vertex where the contribution gets high
        (CURRENTLY NOT USED)
        :param path_key_list:
        :param render_data:
        :return:
        """
        # test just first index

        if not len(path_key_list) > 0:
            return []

        outliers_tpl_list = []
        for path_idx in path_key_list:
            # get path
            path_data = render_data.dict_paths.get(path_idx, None)
            verts_dict = path_data.dict_vertices

            # soft detection find index with largest gradient to previous value
            detection_vert_key = -1
            diff_prev = 0
            for key, vert in verts_dict.items():
                v_prev = verts_dict.get(key-1, None)
                if v_prev:
                    if v_prev.is_li_set and vert.is_li_set:
                        diff = abs(v_prev.li.mean - vert.li.mean)
                        if diff > diff_prev:
                            diff_prev = diff
                            detection_vert_key = key

            outliers_tpl_list.append((path_idx, detection_vert_key))

        return outliers_tpl_list

    def run_outlier_detection(self, data):
        """
        Runs the outlier detection on the given data set
        :param data: final_estimate data
        :return:
        """
        if not self._active:
            return np.array([], dtype=np.int32)

        if self._default:
            self._path_outlier_key_list = self.default_outlier_detection(data)
        else:
            self._path_outlier_key_list = self.esd_outlier_detection(data)
        logging.info("Outliers keys={}".format(self._path_outlier_key_list))

    def default_outlier_detection(self, data):
        """
        Default outlier detection
        :param data:
        :return:
        """
        start = time.time()
        # https://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
        outliers = data[abs(data - np.mean(data)) > self._m * np.std(data)]
        outliers_keys = np.array([], dtype=np.int32)
        for o in outliers:
            outliers_keys = np.append(outliers_keys, np.where(data == o))
        logging.info('default outlier detection runtime: {}ms'.format(time.time() - start))
        return outliers_keys

    def esd_outlier_detection(self, data):
        """
        Outlier detection with Generalized ESD from Rosner 1983
        :param data:
        :return:
        """
        # compute outliers with Generalized ESD from Rosner 1983
        start = time.time()
        outliers = self.generalized_esd_test(data, self._alpha, self._k)
        logging.info('esd outlier detection runtime: {}ms'.format(time.time() - start))
        return np.append(np.array([], dtype=np.int32), outliers[1])

    @staticmethod
    def generalized_esd_test(data, alpha=0.05, max_o=1):

        """
        Runs the Generalized ESD algorithm by Rosner
        :param data:
        :param alpha:
        :param max_o:
        :return:
        """

        from scipy.stats import t
        import numpy.ma as ma

        xm = ma.array(data)
        n = len(xm)

        # Compute R-values
        R = []
        L = []
        minds = []
        for i in smo.range(max_o + 1):
            # Compute mean and std of x
            xmean = xm.mean()
            xstd = xm.std()
            # Find maximum deviation
            rr = np.abs((xm - xmean) / xstd)
            minds.append(np.argmax(rr))
            R.append(rr[minds[-1]])
            if i >= 1:
                p = 1.0 - alpha / (2.0 * (n - i + 1))
                perPoint = t.ppf(p, n - i - 1)
                L.append((n - i) * perPoint / np.sqrt((n - i - 1 + perPoint ** 2) * (n - i + 1)))
            # Mask that value and proceed
            xm[minds[-1]] = ma.masked
        # Remove the first entry from R, which is of
        # no meaning for the test
        R.pop(-1)
        # Find the number of outliers
        outliers_found = False
        for i in smo.range(max_o - 1, -1, -1):
            if R[i] > L[i]:
                outliers_found = True
                break
        # Prepare return value
        if outliers_found:
            return i + 1, minds[0:i + 1]
        else:
            # No outliers could be detected
            return 0, []
