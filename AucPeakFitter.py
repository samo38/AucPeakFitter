from MainUi import Ui_MainWindow

from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6 import QtGui
import sys


class Window(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    win = Window()
    win.show()
    sys.exit(app.exec())
