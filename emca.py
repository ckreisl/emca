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
