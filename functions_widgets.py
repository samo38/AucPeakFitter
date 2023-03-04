import numpy as np
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

    sig_pick_line = Signal(int, float)
    sig_pick_region = Signal(int, float, float)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.gauss = dms.Gaussian()
        self.x_min = None
        self.x_max = None
        self.x_mid = None
        self.line = None
        self.region = None

        self.pb_cent_val.clicked.connect(self.slt_pick_cent)
        self.pb_cent_mm.clicked.connect(self.slt_pick_reg)
        self.fix_sigma.stateChanged.connect(self.slt_fix_sigma)
        self.fix_amp.stateChanged.connect(self.slt_fix_amp)

    @Slot(int)
    def slt_fix_amp(self, state):
        if state == Qt.Unchecked.value:
            self.le_amp.clear()
            self.le_amp.setReadOnly(True)
        elif state == Qt.Checked.value:
            self.le_amp.clear()
            self.le_amp.setReadOnly(False)

    @Slot(int)
    def slt_fix_sigma(self, state):
        if state == Qt.Unchecked.value:
            self.le_sigma.clear()
            self.le_sigma.setReadOnly(True)
        elif state == Qt.Checked.value:
            self.le_sigma.clear()
            self.le_sigma.setReadOnly(False)

    @Slot(bool)
    def slt_pick_cent(self, checked):
        if checked:
            self.pb_cent_val.setText("Apply")
            self.pb_cent_val.setStyleSheet(u"background-color: rgb(246, 97, 81);")
            self.sig_pick_line.emit(1, self.x_mid)
        else:
            self.pb_cent_val.setText("Set")
            self.pb_cent_val.setStyleSheet(u"background-color: ;")
            self.sig_pick_line.emit(0, 0)
            self.gauss.center.value = self.line
            self.le_cent_val.setText(f"{self.line: .3f}")
            self.le_cent_val.setCursorPosition(0)

    @Slot(bool)
    def slt_pick_reg(self, checked):
        if checked:
            self.pb_cent_mm.setText("Apply")
            self.pb_cent_mm.setStyleSheet(u"background-color: rgb(246, 97, 81);")
            self.sig_pick_region.emit(1, self.x_min, self.x_max)
        else:
            self.pb_cent_mm.setText("Set")
            self.pb_cent_mm.setStyleSheet(u"background-color: ;")
            self.sig_pick_region.emit(0, 0, 0)
            val1 = self.region[0]
            val2 = self.region[1]
            self.gauss.center.min = val1
            self.gauss.center.max = val2
            self.le_cent_mm.setText(f"{val1: .3f}-{val2: .3f}")
            self.le_cent_mm.setCursorPosition(0)

    def set_min_mid_max(self, x_arr: np.array):
        self.x_min = x_arr[0]
        self.x_max = x_arr[-1]
        self.x_mid = x_arr[0] + (x_arr[-1] - x_arr[0]) * 0.5

    def set_line(self, value: float):
        self.line = value

    def set_region(self, values: tuple):
        self.region = values

    def fill_widget(self, func: dms.Gaussian):
        self.gauss = func
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
            self.le_amp.setText(f"{amp_val: .3f}")

        if cen_val is None:
            self.le_cent_val.clear()
        else:
            self.le_cent_val.setText(f"{cen_val: .3f}")

        if (cen_max is None) or (cen_min is None):
            self.le_cent_mm.clear()
        else:
            self.le_cent_mm.setText(f"{cen_min: .3f}-{cen_max: .3f}")

        if sigma_val is None:
            self.le_sigma.clear()
        else:
            self.le_sigma.setText(f"{sigma_val: .3f}")

    def get_params(self):
        if len(self.le_cent_val.text()) == 0:
            QMessageBox.warning(self, "Error!", "Set the value of the Gaussian center!")
            return None
        if len(self.le_cent_mm.text()) == 0 and (not self.fix_center.isChecked()):
            QMessageBox.warning(self, "Error!", "Set the min-max value of the Gaussian center!")
            return None
        if self.fix_sigma.isChecked() and len(self.le_sigma) == 0:
            QMessageBox.warning(self, "Error!", "Set the value of the Gaussian sigma!")
            return None
        if self.fix_amp.isChecked() and len(self.le_amp) == 0:
            QMessageBox.warning(self, "Error!", "Set the value of the Gaussian amplitude!")
            return None
        sigma_val = str_to_float(self.le_sigma.text())
        amplitude_val = str_to_float(self.le_amp.text())
        if sigma_val is False:
            QMessageBox.warning(self, "Error!", "Enter a float number for sigma!")
        if amplitude_val is False:
            QMessageBox.warning(self, "Error!", "Enter a float number for amplitude!")
        if (sigma_val is False) or (amplitude_val is False):
            return
        self.gauss.center.value = self.line
        self.gauss.center.min = self.region[0]
        self.gauss.center.max = self.region[1]
        self.gauss.center.fixed = self.fix_center.checkState() == Qt.Checked.value

        self.gauss.sigma.fixed = self.fix_sigma.checkState() == Qt.Checked.value
        self.gauss.sigma.bound = self.bound_sigma.checkState() == Qt.Checked.value
        self.gauss.sigma.value = sigma_val

        self.gauss.amplitude.fixed = self.fix_sigma.checkState() == Qt.Checked.value
        self.gauss.amplitude.value = amplitude_val

        return self.gauss


class ExponentialControl(QWidget, gui_exponential.Ui_Form):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.exp = dms.Exponential()

        self.fix_amp.stateChanged.connect(self.slt_fix_amp)
        self.fix_decay.stateChanged.connect(self.slt_fix_decay)

    @Slot(int)
    def slt_fix_amp(self, state):
        if state == Qt.Unchecked.value:
            self.le_amp.clear()
            self.le_amp.setReadOnly(True)
        elif state == Qt.Checked.value:
            self.le_amp.clear()
            self.le_amp.setReadOnly(False)

    @Slot(int)
    def slt_fix_decay(self, state):
        if state == Qt.Unchecked.value:
            self.le_decay.clear()
            self.le_decay.setReadOnly(True)
        elif state == Qt.Checked.value:
            self.le_decay.clear()
            self.le_decay.setReadOnly(False)

    def fill_widget(self, func: dms.Exponential):
        self.exp = func
        amp_fixed = self.exp.amplitude.fixed
        amp_val = self.exp.amplitude.value

        dec_fixed = self.exp.decay.fixed
        dec_val = self.exp.decay.value
        self.fix_amp.setChecked(amp_fixed)
        self.fix_decay.setChecked(dec_fixed)

        if amp_val is None:
            self.le_amp.clear()
        else:
            self.le_amp.setText(f"{amp_val: .3f}")

        if dec_val is None:
            self.le_decay.clear()
        else:
            self.le_decay.setText(f"{dec_val: .3f}")

    def get_params(self):
        if self.fix_decay.isChecked() and len(self.le_decay) == 0:
            QMessageBox.warning(self, "Error!", "Set the value of the Exponential decay!")
            return None
        if self.fix_amp.isChecked() and len(self.le_amp) == 0:
            QMessageBox.warning(self, "Error!", "Set the value of the Exponential amplitude!")
            return None

        amplitude_val = str_to_float(self.le_amp.text())
        decay_val = str_to_float(self.le_decay.text())
        if decay_val is False:
            QMessageBox.warning(self, "Error!", "Enter a float number for decay!")
        if amplitude_val is False:
            QMessageBox.warning(self, "Error!", "Enter a float number for amplitude!")
        if (decay_val is False) or (amplitude_val is False):
            return

        self.exp.amplitude.fixed = self.fix_amp.checkState() == Qt.Checked.value
        self.exp.amplitude.value = amplitude_val

        self.exp.decay.fixed = self.fix_decay.checkState() == Qt.Checked.value
        self.exp.decay.value = decay_val

        return self.exp


