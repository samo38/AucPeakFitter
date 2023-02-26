from PySide6 import QtWidgets
import gui_gaussian
import gui_exponential


class GaussianControl(QtWidgets.QWidget, gui_gaussian.Ui_Form):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class ExponentialControl(QtWidgets.QWidget, gui_exponential.Ui_Form):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
