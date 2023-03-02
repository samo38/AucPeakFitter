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
import pyqtgraph
import numpy as np
from auc_data_io import AucRawData
import gui_import
import gui_species_list
import gui_species_control
import data_models as dms


class SpeciesControl(QFrame, gui_species_control.Ui_Frame):

    sig_pick_line = Signal(int, float)
    sig_pick_region = Signal(int, float, float)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.icon_vis = QIcon()
        self.icon_vis.addFile(u":/Icon/Resources/Icons/visibility_FILL0_wght400_GRAD0_opsz48.svg",
                              QSize(), QIcon.Normal, QIcon.Off)
        self.icon_invis = QIcon()
        self.icon_invis.addFile(u":/Icon/Resources/Icons/visibility_off_FILL0_wght400_GRAD0_opsz48.svg",
                                QSize(), QIcon.Normal, QIcon.Off)

        self.cmb_type.clear()
        self.cmb_type.addItem("Gaussian")
        self.cmb_type.addItem("Exponential")

        self.model = dms.Model(dms.Types.EMPTY)

        self.vis_state = True
        self.x_arr = None
        self.lined_picked = None
        self.region_picked = None
        self.cmb_type.currentTextChanged.connect(self.slt_func_updated)
        self.wg_gaus.pb_cent_val.clicked.connect(self.slt_set_gauss_cent)
        self.pb_vis.clicked.connect(self.slt_update_vis)
        self.cmb_type.setCurrentIndex(0)
        self.slt_func_updated('Gaussian')

    @Slot(str)
    def slt_func_updated(self, text):
        if text == 'Gaussian':
            self.stacked.setCurrentWidget(self.wg_gaus)
            self.model = dms.Model(dms.Types.GAUSS)
        elif text == 'Exponential':
            self.stacked.setCurrentWidget(self.wg_exp)
            self.model = dms.Model(dms.Types.EXP)

    @Slot(bool)
    def slt_set_gauss_cent(self, checked):
        if checked:
            self.wg_gaus.pb_cent_val.setText("Apply")
            self.wg_gaus.pb_cent_val.setStyleSheet(u"background-color: rgb(246, 97, 81);")
            # val = (self.x_arr[-1] - self.x_arr[0]) / 2.0
            # val += self.x_arr[0]
            val = 6.5
            self.sig_pick_line.emit(1, val)
            # self.wg_plot.pick_line_trim(1, val)
        else:
            self.wg_gaus.pb_cent_val.setText("Set")
            self.wg_gaus.pb_cent_val.setStyleSheet(u"background-color: ;")
            self.sig_pick_line.emit(0, 0)
            # self.wg_plot.pick_line_trim(0, 0)
            # val = self.wg_plot.picker_line_trim_val
            self.sig_pick_line.emit(0, 0)
            self.model.params.center = self.lined_picked
            self.wg_gaus.le_cent_val.setText(f"{self.lined_picked: .3f}")
            self.wg_gaus.le_cent_val.setCursorPosition(0)

    @Slot(bool)
    def slt_update_vis(self):
        self.vis_state = not self.vis_state
        self.change_vis_btn(self.vis_state)
        self.model.visible = self.vis_state

    def change_vis_btn(self, state: bool):
        if state:
            self.pb_vis.setText("ON")
            self.pb_vis.setIcon(self.icon_vis)
            self.pb_vis.setStyleSheet("background-color: ;")
        else:
            self.pb_vis.setText("OFF")
            self.pb_vis.setIcon(self.icon_invis)
            self.pb_vis.setStyleSheet("background-color: rgb(220,220,220);")

    def set_model(self, model=None):
        if model is None:
            self.model = dms.Model(dms.Types.GAUSS)
            self.cmb_type.setCurrentIndex(0)
            self.fill_gauss()
        else:
            if model.type == dms.Types.EMPTY:
                self.set_model(None)
                return
            self.model = model
            if model.type == dms.Types.GAUSS:
                self.fill_gauss()
            elif model.type == dms.Types.EXP:
                self.fill_exp()
        self.vis_state = self.model.visible
        self.le_name.setText(self.model.name)
        self.change_vis_btn(self.vis_state)

    def get_model(self):
        return self.model

    def fill_gauss(self):
        amp_fixed = self.model.params.amplitude.fixed
        amp_val = self.model.params.amplitude.value

        cen_fixed = self.model.params.center.fixed
        cen_val = self.model.params.center.value
        cen_min = self.model.params.center.min
        cen_max = self.model.params.center.max

        sig_fixed = self.model.params.sigma.fixed
        sig_val = self.model.params.sigma.value
        sig_bound = self.model.params.sigma.bound

        if amp_fixed:
            self.wg_gaus.fix_amp.setChecked(True)
        else:
            self.wg_gaus.fix_amp.setChecked(False)

        if cen_fixed:
            self.wg_gaus.fix_center.setChecked(True)
        else:
            self.wg_gaus.fix_center.setChecked(False)

        if sig_fixed:
            self.wg_gaus.fix_sigma.setChecked(False)
        else:
            self.wg_gaus.fix_sigma.setChecked(False)

        if amp_val is None:
            self.wg_gaus.le_amp.clear()
        else:
            self.wg_gaus.le_amp.setText(f"{amp_val: .3f}")

        if cen_val is None:
            self.wg_gaus.le_cent_val.clear()
        else:
            self.wg_gaus.le_cent_val.setText(f"{cen_val: .3f}")

        if (cen_max is None) or (cen_min is None):
            self.wg_gaus.le_cent_mm.clear()
        else:
            self.wg_gaus.le_cent_mm.setText(f"{cen_min: .3f}-{cen_max: .3f}")

        if sig_val is None:
            self.wg_gaus.le_sigma.clear()
        else:
            self.wg_gaus.le_sigma.setText(f"{sig_val: .3f}")

        if sig_bound:
            self.wg_gaus.bound_sigma.setChecked(True)
        else:
            self.wg_gaus.bound_sigma.setChecked(False)

    def fill_exp(self):
        amp_fixed = self.model.params.amplitude.fixed
        amp_val = self.model.params.amplitude.value

        dec_fixed = self.model.params.center.fixed
        dec_val = self.model.params.center.value

        if amp_fixed:
            self.wg_exp.fix_amp.setChecked(True)
        else:
            self.wg_exp.fix_amp.setChecked(False)

        if dec_fixed:
            self.wg_exp.fix_amp.setChecked(True)
        else:
            self.wg_exp.fix_amp.setChecked(False)

        if amp_val is None:
            self.wg_exp.le_ampl_val.clear()
        else:
            self.wg_exp.le_ampl_val.setText(f"{amp_val: .3f}")

        if dec_val is None:
            self.wg_exp.le_decay_val.clear()
        else:
            self.wg_exp.le_decay_val.setText(f"{dec_val: .3f}")

    def set_x_arr(self, x_arr: np.array):
        self.x_arr = x_arr

