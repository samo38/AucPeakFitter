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


class ImportWidget(QFrame, gui_import.Ui_Frame):

    sig_new_file = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.temperature = None
        self.rpm = None
        self.wavelength = None

        self.pb_open.clicked.connect(self.slt_open)

    @Slot(object)
    def slt_open(self):
        home_dir = QDir.homePath()
        dialog_output = QFileDialog.getOpenFileName(self, "Open AUC File", home_dir, "(*.auc)")
        file_name = dialog_output[0]
        if len(file_name) == 0:
            return
        auc_data = AucRawData()
        state = auc_data.read(file_name)
        if not state:
            msg = f"The following file is not readable by this program:\n{file_name}"
            QMessageBox.warning(self, "Warning!", msg)
            return
        self.le_desc.setText(auc_data.description)
        self.le_type.setText(auc_data.type)
        self.le_cell.setText(str(auc_data.cell))
        self.le_chan.setText(auc_data.channel)
        self.temperature = auc_data.temperature
        self.rpm = auc_data.rpm
        self.wavelength = auc_data.wavelength
        x_values = auc_data.xvalues
        y_values = auc_data.rvalues
        n_scans = len(y_values)
        all_data_models = []
        for i in range(n_scans):
            data_models = dms.DataModels()
            data_models.set_raw(x_values, y_values[i])
            data_models.set_trim(x_values, y_values[i])
            all_data_models.append(data_models)
        self.sig_new_file.emit(all_data_models)

    def update_info(self, n: int):
        rpm = self.rpm[n] / 1000
        self.le_rpm.setText(f"{rpm: g}k")
        wave = self.wavelength[n]
        self.le_wavl.setText(f"{wave: g}")
        temp = self.temperature[n]
        self.le_temp.setText(f"{temp: g}")


class SpeciesList(QFrame, gui_species_list.Ui_Frame):

    sig_new_scan_id = Signal(int)
    sig_new_species = Signal()
    sig_species_id = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.spin_box.valueChanged.connect(self.slt_new_sb_id)
        self.lw_species.currentRowChanged.connect(self.slt_species_changed)

    @Slot(int)
    def slt_new_sb_id(self, n: int):
        self.sig_new_scan_id.emit(n - 1)

    @Slot(int)
    def slt_species_changed(self, row):
        n_items = self.lw_species.count()
        if row == (n_items - 1):
            self.sig_new_species.emit()
        else:
            self.sig_species_id.emit(row)

    def set_spin_box(self, n: int):
        self.spin_box.valueChanged.disconnect(self.slt_new_sb_id)
        self.spin_box.clear()
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(n)
        self.spin_box.valueChanged.connect(self.slt_new_sb_id)
        self.spin_box.setValue(n)

    def set_species_list(self, items: list):
        self.lw_species.currentRowChanged.disconnect(self.slt_species_changed)
        self.lw_species.clear()
        for i in range(len(items)):
            self.lw_species.addItem(items[i])
        self.lw_species.currentRowChanged.connect(self.slt_species_changed)


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

        self.gauss_model = dms.Model("GAUSS")
        self.exp_model = dms.Model("EXP")

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
            self.gauss_model = dms.Model("GAUSS")
        elif text == 'Exponential':
            self.stacked.setCurrentWidget(self.wg_exp)
            self.exp_model = dms.Model("EXP")

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
        if self.cmb_type.currentText() == "Gaussian":
            self.gauss_model.visible = self.vis_state
        elif self.cmb_type.currentText() == "Exponential":
            self.exp_model = self.vis_state

    def change_vis_btn(self, state: bool):
        if state:
            self.pb_vis.setText("ON")
            self.pb_vis.setIcon(self.icon_vis)
            self.pb_vis.setStyleSheet("background-color: ;")
        else:
            self.pb_vis.setText("OFF")
            self.pb_vis.setIcon(self.icon_invis)
            self.pb_vis.setStyleSheet("background-color: rgb(220,220,220);")

    def setup_widget(self, model=None):
        if model is None:
            self.vis_state = True
            self.gauss_model = dms.Model("GAUSS")
            self.stacked.setCurrentWidget(self.wg_gaus)
            self.fill_gauss()
            self.le_name.setText(self.gauss_model.name)
        else:
            if model.type == "GAUSS":
                self.gauss_model = model
                self.fill_gauss()
                self.le_name.setText(self.gauss_model.name)
                self.vis_state = self.gauss_model.visible

            elif model.type == "EXP":
                self.exp_model = model
                self.fill_exp()
                self.le_name.setText(self.exp_model.name)
                self.vis_state = self.exp_model.visible
        self.change_vis_btn(self.vis_state)

    def fill_gauss(self):
        amp_fixed = self.gauss_model.params.amplitude.fixed
        amp_val = self.gauss_model.params.amplitude.value

        cen_fixed = self.gauss_model.params.center.fixed
        cen_val = self.gauss_model.params.center.value
        cen_min = self.gauss_model.params.center.min
        cen_max = self.gauss_model.params.center.max

        sig_fixed = self.gauss_model.params.sigma.fixed
        sig_val = self.gauss_model.params.sigma.value
        sig_bound = self.gauss_model.params.sigma.bound

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
        amp_fixed = self.gauss_model.params.amplitude.fixed
        amp_val = self.gauss_model.params.amplitude.value

        dec_fixed = self.gauss_model.params.center.fixed
        dec_val = self.gauss_model.params.center.value

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

    def set_model(self, model: dms.Model):
        if model.type == "GAUSS":
            self.gauss_model = model
        elif model.type == "EXP":
            self.exp_model = model

    # def get_model(self):
    #     return self.model

    def set_x_arr(self, x_arr: np.array):
        self.x_arr = x_arr


class PlotWidget(QFrame):

    sig_data_updated = Signal()
    sig_line_picked = Signal()
    sig_region_picked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(1)

        self.x_raw = None
        self.y_raw = None
        self.x_trim = None
        self.y_trim = None
        self.region_values = None
        self.line_value = None

        plt_win = pyqtgraph.GraphicsLayoutWidget()
        self.plt_species = plt_win.addPlot(title="Trimmed & Decomposed")  # PlotItem
        self.plt_import = plt_win.addPlot(title="Imported")
        plt_win.nextRow()
        self.plt_error = plt_win.addPlot(title="Residuals")
        self.plt_model = plt_win.addPlot(title="Trimmed & Modeled")

        self.icon_check = QIcon()
        self.icon_check.addFile(u":/Icon/Resources/Icons/check_circle_FILL0_wght400_GRAD0_opsz48.svg",
                                     QSize(), QIcon.Normal, QIcon.Off)
        self.icon_region = QIcon()
        self.icon_region.addFile(u":/Icon/Resources/Icons/horizontal_distribute_FILL0_wght400_GRAD0_opsz48.svg",
                                     QSize(), QIcon.Normal, QIcon.Off)
        self.icon_cancel = QIcon()
        self.icon_cancel.addFile(u":/Icon/Resources/Icons/cancel_FILL0_wght400_GRAD0_opsz48.svg",
                                 QSize(), QIcon.Normal, QIcon.Off)

        self.pb_region = QPushButton(u"Region")
        self.pb_region.setCheckable(True)
        self.pb_region.setIcon(self.icon_region)
        self.pb_region.setStyleSheet(u"background-color: rgb(249, 240, 107);")
        self.pb_region.setIconSize(QSize(16, 16))

        self.pb_set_region = QPushButton("Apply")
        self.pb_set_region.setEnabled(False)
        self.pb_set_region.setIcon(self.icon_check)
        self.pb_set_region.setIconSize(QSize(16, 16))

        lyt_pb = QVBoxLayout()
        lyt_pb.setContentsMargins(0, 0, 0, 0)
        lyt_pb.setSpacing(1)
        lyt_pb.addWidget(self.pb_region)
        lyt_pb.addWidget(self.pb_set_region)
        lyt_pb.addStretch(1)

        self.curve_import = self.plt_import.plot(pen='y')  # PlotDataItem
        self.curve_trim = self.plt_species.plot(pen='y')
        self.curve_species = []
        self.curve_residue = self.plt_error.plot(pen='g')
        self.curve_model_data = self.plt_model.plot(pen='y')
        self.curve_model_fit = self.plt_model.plot(pen='r')

        self.region_picker_import = pyqtgraph.LinearRegionItem(pen="white")
        self.region_picker_trim = pyqtgraph.LinearRegionItem(pen="white")
        self.line_picker_trim = pyqtgraph.InfiniteLine(pen="white", movable=True)
        # self.picker_raw.setZValue(-10)

        layout = QHBoxLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.addWidget(plt_win)
        layout.addLayout(lyt_pb)
        self.setLayout(layout)

        self.region_picker_import.sigRegionChanged.connect(self.update_trim)
        self.pb_region.clicked.connect(self.update_region)
        self.pb_set_region.clicked.connect(self.set_region)

    @Slot(object)
    def update_trim(self):
        [min_val, max_val] = self.region_picker_import.getRegion()
        ind = np.logical_and(self.x_raw >= min_val, self.x_raw <= max_val)
        x_temp = self.x_raw[ind]
        y_temp = self.y_raw[ind]
        self.plot_trim(x_temp, y_temp)

    @Slot(bool)
    def update_region(self, checked):
        # self.pb_reg.setIconSize(QSize(16, 16))
        if checked:
            self.pb_region.setText("Cancel")
            self.pb_region.setIcon(self.icon_cancel)
            self.pb_region.setStyleSheet(u"background-color: rgb(246, 97, 81);")
            self.pb_set_region.setStyleSheet(u"background-color: rgb(143, 240, 164);")
            self.pb_set_region.setEnabled(True)
            self.pick_region_import(1)
        else:
            self.pb_region.setText("Region")
            self.pb_region.setIcon(self.icon_region)
            self.pb_region.setStyleSheet(u"background-color: rgb(249, 240, 107);")
            self.pb_set_region.setStyleSheet(u"background-color: ;")
            self.pb_set_region.setEnabled(False)
            self.pick_region_import(-1)

    @Slot()
    def set_region(self):
        self.pb_region.setText("Region")
        self.pb_region.setChecked(False)
        self.pb_region.setIcon(self.icon_region)
        self.pb_region.setStyleSheet(u"background-color: rgb(249, 240, 107);")
        self.pb_set_region.setStyleSheet(u"background-color: ;")
        self.pb_set_region.setEnabled(False)
        self.pick_region_import(0)

    def set_data(self, x_raw: np.array, y_raw: np.array, x_trim: np.array, y_trim: np.array):
        self.x_raw = x_raw
        self.y_raw = y_raw
        self.x_trim = x_trim
        self.y_trim = y_trim
        self.plot_raw()
        self.plot_trim()

    def get_data(self):
        return self.x_raw, self.y_raw, self.x_trim, self.y_trim

    def plot_raw(self):
        self.curve_import.setData(self.x_raw, self.y_raw)

    def plot_trim(self, x=None, y=None):
        if (x is not None) and (y is not None):
            self.curve_trim.setData(x, y)
        else:
            self.curve_trim.setData(self.x_trim, self.y_trim)

    def pick_region_import(self, state: int):
        if state == 1:  # connect picker
            self.region_picker_import.setRegion([np.min(self.x_trim), np.max(self.x_trim)])
            self.plt_import.addItem(self.region_picker_import)
        elif state == -1:  # cancel and close piker
            self.plt_import.removeItem(self.region_picker_import)
            self.plot_trim()
        elif state == 0:  # accept and close picker
            data = self.curve_trim.getData()
            self.x_trim = data[0]
            self.y_trim = data[1]
            self.plt_import.removeItem(self.region_picker_import)
            self.sig_data_updated.emit()

    def pick_region_trim(self, state: int, x1: float, x2: float):
        if state == 1:  # connect picker
            self.region_picker_trim.setRegion([x1, x2])
            self.plt_species.addItem(self.region_picker_trim)
        elif state == 0:  # accept and close picker
            self.region_values = self.region_picker_trim.getRegion()
            self.plt_species.removeItem(self.region_picker_trim)
            self.sig_region_picked.emit()

    def pick_line_trim(self, state: int, value: float):
        if state == 1:
            self.line_picker_trim.setValue(value)
            self.plt_species.addItem(self.line_picker_trim)
        elif state == 0:
            self.line_value = self.line_picker_trim.value()
            self.plt_species.removeItem(self.line_picker_trim)
            self.sig_line_picked.emit()



