"""
    This file is part of EMCA, an explorer of Monte-Carlo based Algorithms.
    Copyright (c) 2019-2020 by Christoph Kreisl and others.
    EMCA is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License Version 3
    as published by the Free Software Foundation.
    EMCA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np
import logging
import time


class FinalEstimate(object):

    """
        FinalEstimate
        Represents all final estimate values of n traced paths where n stands for the amount of samples.
        A final estimate value is represented by a color3f type.
    """

    def __init__(self, dict_paths):

        start = time.time()

        # index shift by 1
        offset = 0
        self._x_list = np.array(list(dict_paths.keys())) + offset

        # collect final estimates of all paths,
        # if one final estimate is not set take [-1,-1,-1, 1] as value
        estimates = []
        for key, path in dict_paths.items():
            if not path.final_estimate:
                logging.info('no final estimate set on server')
                estimates.append([-1, -1, -1, 1])
                continue
            estimates.append(list(path.final_estimate))

        self._y_list = np.array(estimates)

        # get r,g,b values final estimate
        self._r = self._y_list[:, 0]
        self._g = self._y_list[:, 1]
        self._b = self._y_list[:, 2]

        # compute the mean of all rgb values
        self._mean = np.mean(self._y_list, axis=1)

        logging.info('generated plot data in: {}ms'.format(time.time() - start))

    def is_valid(self):
        """
        Checks if the dataset is valid
        :return:
        """
        return self._x_list.shape[0] == self._y_list.shape[0]

    @property
    def plot_data_x(self):
        """
        Returns the values of the x-axis as a numpy array
        :return:
        """
        return self._x_list

    @property
    def plot_data_y(self):
        """
        Returns the values of all final estimate values as a numpy array
        :return:
        """
        return self._y_list

    @property
    def red(self):
        """
        Returns the red values of all final estimate values as a numpy array
        :return:
        """
        return self._r

    @property
    def green(self):
        """
        Returns the green values of all final estimate values as a numpy array
        :return:
        """
        return self._g

    @property
    def blue(self):
        """
        Returns the blue values of all final estimate values as a numpy array
        :return:
        """
        return self._b

    @property
    def mean(self):
        """
        Returns the mean of all final estimate values as a numpy array
        :return:
        """
        return self._mean

    def clear(self):
        """
        Clears all data sets
        :return:
        """
        self._x_list = None
        self._y_list = None
        self._mean = None
        self._r = None
        self._g = None
        self._b = None
