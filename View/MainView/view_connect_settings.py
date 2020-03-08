from PyQt5 import uic
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
import logging


class ViewConnectSettings(QWidget):

    """
        ViewConnectSettings
        Handles the connect settings view
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=None)
        uic.loadUi('View/ui/connect.ui', self)

        self._controller = None

        # center widget depending on screen size
        desktop_widget = QApplication.desktop()
        screen_rect = desktop_widget.availableGeometry(self)
        self.move(screen_rect.center() - self.rect().center())

        try:
            self._hostname = self.leHostname.text()
            self._port = int(self.lePort.text())
        except ValueError as e:
            logging.error(e)

        self.btnConnect.clicked.connect(self.btn_connect)

    def set_controller(self, controller):
        """
        Set the connection to the controller
        :param controller: Controller
        :return:
        """
        self._controller = controller

    def keyPressEvent(self, event):
        """
        Handles key press event. If the enter button is clicked the connect button is triggered
        :param event:
        :return:
        """
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.btn_connect(True)

    @pyqtSlot(bool, name='connect')
    def btn_connect(self, clicked):
        """
        Informs the controller to connect to the given hostname and port.
        Closes the view afterwards.
        :param clicked: boolean
        :return:
        """
        logging.info('Clicked connect btn, show connect view')
        try:
            self._hostname = self.leHostname.text()
            self._port = int(self.lePort.text())
        except ValueError as e:
            logging.error(e)
            return None

        self._controller.handle_connect(self._hostname, self._port)
        self.close()

