from gui_main_window import Ui_MainWindow
from PySide6 import QtWidgets


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

