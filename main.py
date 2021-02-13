import os
import sys

import qdarkstyle
from PyQt5.QtWidgets import QApplication

from ExifModel import ExifModel
from ExifController import ExifController
from ExifView import ExifView

os.environ['QT_MAC_WANTS_LAYER'] = '1'

if __name__ == '__main__':

    model = ExifModel()
    controller = ExifController(model)
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = ExifView(controller)

    sys.exit(app.exec_())