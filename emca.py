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

from PyQt5.QtWidgets import QApplication
from Core.logger import InitLogSystem
import sys

from Model.dataset import Dataset
from View.MainView.main_view import MainView
from Controller.controller import Controller


class EMCAClient(object):

    """
        Explorer of Monte-Carlo based Algorithms - Client
    """

    def __init__(self):
        self.model = Dataset()
        self.view = MainView()
        self.controller = Controller(self.model, self.view)

    def start(self):
        """
        Starts and opens the GUI of EMCA
        :return:
        """
        self.controller.display_view()
        #autoconnect to localhost on startup
        self.controller.handle_connect("localhost", 50013)


if __name__ == '__main__':
    InitLogSystem()
    app = QApplication(sys.argv)
    emca_client = EMCAClient()
    emca_client.start()
    sys.exit(app.exec_())