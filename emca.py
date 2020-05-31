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

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QTextStream
from Core.logger import InitLogSystem
import sys

from Model.model import Model
from View.MainView.main_view import MainView
from Controller.controller import Controller
import Resources.breeze_resources


class EMCAClient(object):

    """
        Explorer of Monte-Carlo based Algorithms - Client
    """

    def __init__(self):
        self.model = Model()
        self.view = MainView()
        self.controller = Controller(self.model, self.view)

    def load_theme(self, qt_app):
        theme = self.model.options_data.get_theme()
        if theme == 'light':
            theme_files = "./Resources/light.qss"
        else:
            theme_files = "./Resources/dark.qss"
        file = QFile(theme_files)
        file.open(QFile.ReadOnly | QFile.Text)
        text_stream = QTextStream(file)
        qt_app.setStyleSheet(text_stream.readAll())
        self.controller.apply_theme(theme)

    def start(self):
        """
        Starts and opens the GUI of EMCA
        :return:
        """
        self.controller.display_view()


if __name__ == '__main__':
    InitLogSystem()
    app = QApplication(sys.argv)
    emca_client = EMCAClient()
    emca_client.load_theme(app)
    emca_client.start()
    sys.exit(app.exec_())
