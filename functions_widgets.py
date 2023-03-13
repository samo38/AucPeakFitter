from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QDir,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy, QFileDialog, QMessageBox,
    QSpinBox, QVBoxLayout, QWidget)
from PySide6.QtCore import (Slot, Signal)
import numpy as np
import copy
import gui_gaussian
import gui_exponential
import data_models as dms


def str_to_float(x: str):
    if len(x) == 0:
        return None
    try:
        f_x = float(x)
        return f_x
    except ValueError:
        return False


class GaussianControl(QWidget, gui_gaussian.Ui_Form):

    sig_pick_params = Signal(int, float, float, float)
    sig_set_enable = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.gauss = dms.Gaussian()
        self.line = None
        self.region = None

        # self.pb_cent_val.clicked.connect(self.slt_pick_cent)
        self.pb_cent_mm.clicked.connect(self.slt_pick_params)
        self.fix_center.stateChanged.connect(self.slt_fix_center)
        self.fix_sigma.stateChanged.connect(self.slt_fix_sigma)
        self.fix_amp.stateChanged.connect(self.slt_fix_amp)
        self.bound_sigma.stateChanged.connect(self.slt_bound_sigma)
        self.main_sigma.stateChanged.connect(self.slt_main_sigma)
        self.le_amp.editingFinished.connect(self.slt_new_amplitude)
        self.le_sigma.editingFinished.connect(self.slt_new_sigma)

    @Slot(int)
    def slt_fix_center(self, state):
        if state == Qt.Unchecked.value:
            self.gauss.center.fixed = False
        elif state == Qt.Checked.value:
            self.gauss.center.fixed = True

    @Slot(int)
    def slt_fix_amp(self, state):
        if state == Qt.Unchecked.value:
            self.gauss.amplitude.fixed = False
        elif state == Qt.Checked.value:
            self.gauss.amplitude.fixed = True

    @Slot(int)
    def slt_fix_sigma(self, state):
        if state == Qt.Unchecked.value:
            self.gauss.sigma.fixed = False
        elif state == Qt.Checked.value:
            self.gauss.sigma.fixed = True

    @Slot(int)
    def slt_bound_sigma(self, state):
        if state == Qt.Unchecked.value:
            self.gauss.sigma.bound = False
            self.fix_sigma.setChecked(False)
            self.fix_sigma.setEnabled(True)
        elif state == Qt.Checked.value:
            self.gauss.sigma.bound = True
            self.fix_sigma.setChecked(True)
            self.fix_sigma.setDisabled(True)

    @Slot(int)
    def slt_main_sigma(self, state):
        if state == Qt.Unchecked.value:
            self.gauss.main = False
            self.bound_sigma.setEnabled(True)
        elif state == Qt.Checked.value:
            self.gauss.main = True
            self.bound_sigma.setChecked(False)
            self.bound_sigma.setDisabled(True)

    @Slot(bool)
    def slt_pick_params(self, checked):
        if checked:
            self.pb_cent_mm.setText("Apply")
            self.pb_cent_mm.setStyleSheet(u"background-color: rgb(246, 97, 81);")
            if self.region is None or self.line is None:
                self.sig_pick_params.emit(1, -1, -1, -1)
            else:
                self.sig_pick_params.emit(1, self.line, self.region[0], self.region[1])
            self.sig_set_enable.emit(False)
        else:
            self.pb_cent_mm.setText("Set")
            self.pb_cent_mm.setStyleSheet(u"background-color: ;")
            self.sig_pick_params.emit(0, 0, 0, 0)
            self.gauss.center.min = self.region[0]
            self.gauss.center.max = self.region[1]
            self.gauss.center.value = self.line
            self.le_cent_val.setText(f"{self.line:<.3f}")
            self.le_cent_mm.setText(f"{self.region[1]:<.3f} - {self.region[1]:<.3f}")
            self.le_cent_mm.setCursorPosition(0)
            self.sig_set_enable.emit(True)

    @Slot()
    def slt_new_amplitude(self):
        n = str_to_float(self.le_amp.text())
        if n is None:
            self.gauss.amplitude.value = None
        elif n is False:
            amp = self.gauss.amplitude.value
            if amp is None:
                self.le_amp.clear()
            else:
                self.le_amp.setText(f"{amp: .2e}")
        else:
            self.gauss.amplitude.value = n

    @Slot()
    def slt_new_sigma(self):
        n = str_to_float(self.le_sigma.text())
        if n is None:
            self.gauss.sigma.value = None
        elif n is False:
            sigma = self.gauss.sigma.value
            if sigma is None:
                self.le_sigma.clear()
            else:
                self.le_sigma.setText(f"{sigma: .2e}")
        else:
            self.gauss.sigma.value = n

    def set_line(self, value: float):
        self.line = value

    def set_region(self, values: tuple):
        self.region = values

    def fill_widget(self, func: dms.Gaussian, turnoff_main):
        self.gauss = copy.deepcopy(func)
        if turnoff_main:
            self.main_sigma.setChecked(False)
            self.main_sigma.setEnabled(False)
        else:
            if self.gauss.main:
                self.main_sigma.setChecked(True)
            else:
                self.main_sigma.setChecked(False)
            self.main_sigma.setEnabled(True)

        amp_fixed = self.gauss.amplitude.fixed
        amp_val = self.gauss.amplitude.value

        cen_fixed = self.gauss.center.fixed
        cen_val = self.gauss.center.value
        cen_min = self.gauss.center.min
        cen_max = self.gauss.center.max

        sigma_fixed = self.gauss.sigma.fixed
        sigma_val = self.gauss.sigma.value
        sigma_bound = self.gauss.sigma.bound

        self.fix_amp.setChecked(amp_fixed)
        self.fix_center.setChecked(cen_fixed)
        self.fix_sigma.setChecked(sigma_fixed)
        self.bound_sigma.setChecked(sigma_bound)

        if amp_val is None:
            self.le_amp.clear()
        else:
            self.le_amp.setText(f"{amp_val: .2e}")

        if cen_val is None:
            self.le_cent_val.clear()
        else:
            self.le_cent_val.setText(f"{cen_val: .3f}")
        self.line = cen_val

        self.region = None
        if (cen_max is None) or (cen_min is None):
            self.le_cent_mm.clear()
        else:
            self.le_cent_mm.setText(f"{cen_min:<.3f} - {cen_max:<.3f}")
            self.region = (cen_min, cen_max)

        if sigma_val is None:
            self.le_sigma.clear()
        else:
            self.le_sigma.setText(f"{sigma_val: .2e}")

    def get_params(self):
        s = self.gauss.center.value is None
        s = s or self.gauss.center.min is None
        s = s or self.gauss.center.max is None
        if s:
            QMessageBox.warning(self, "Error!", "Set the Gaussian center!")
            return None
        return copy.deepcopy(self.gauss)


class ExponentialControl(QWidget, gui_exponential.Ui_Form):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.exp = dms.Exponential()

        self.fix_amp.stateChanged.connect(self.slt_fix_amp)
        self.fix_decay.stateChanged.connect(self.slt_fix_decay)
        self.le_amp.editingFinished.connect(self.slt_new_amplitude)
        self.le_decay.editingFinished.connect(self.slt_new_decay)

    @Slot(int)
    def slt_fix_amp(self, state):
        if state == Qt.Unchecked.value:
            self.exp.amplitude.fixed = False
        elif state == Qt.Checked.value:
            self.exp.amplitude.fixed = True

    @Slot(int)
    def slt_fix_decay(self, state):
        if state == Qt.Unchecked.value:
            self.exp.decay.fixed = False
        elif state == Qt.Checked.value:
            self.exp.decay.fixed = True

    @Slot()
    def slt_new_amplitude(self):
        n = str_to_float(self.le_amp.text())
        if n is None:
            self.exp.amplitude.value = None
        elif n is False:
            amp = self.exp.amplitude.value
            if amp is None:
                self.le_amp.clear()
            else:
                self.le_amp.setText(f"{amp: .2e}")
        else:
            self.exp.amplitude.value = n

    @Slot()
    def slt_new_decay(self):
        n = str_to_float(self.le_decay.text())
        if n is None:
            self.exp.decay.value = None
        elif n is False:
            sigma = self.exp.decay.value
            if sigma is None:
                self.le_decay.clear()
            else:
                self.le_decay.setText(f"{sigma: .2e}")
        else:
            self.exp.decay.value = n

    def fill_widget(self, func: dms.Exponential):
        self.exp = copy.deepcopy(func)
        amp_fixed = self.exp.amplitude.fixed
        amp_val = self.exp.amplitude.value

        dec_fixed = self.exp.decay.fixed
        dec_val = self.exp.decay.value
        self.fix_amp.setChecked(amp_fixed)
        self.fix_decay.setChecked(dec_fixed)

        if amp_val is None:
            self.le_amp.clear()
        else:
            self.le_amp.setText(f"{amp_val: .2e}")

        if dec_val is None:
            self.le_decay.clear()
        else:
            self.le_decay.setText(f"{dec_val: .2e}")

    def get_params(self):
        return copy.deepcopy(self.exp)


