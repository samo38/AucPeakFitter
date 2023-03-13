import subprocess

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QDir,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy, QFileDialog, QMessageBox,
    QSpinBox, QVBoxLayout, QWidget, QMainWindow, QTextEdit, QDialog, QStyle)
from PySide6.QtCore import (Slot, Signal)
import os
import sys
import numpy as np
import copy
from gui_main_window import Ui_MainWindow
import data_models as dms
from fit_model import FitModel
import lmfit

class UpdateBox(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Software Updating")
        self.setMinimumSize(600, 400)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.pb_close = QPushButton("Close")
        pixmap = QStyle.StandardPixmap.SP_DialogCloseButton
        icon = self.style().standardIcon(pixmap)
        self.pb_close.setIcon(icon)
        lyt = QVBoxLayout()
        lyt.addWidget(self.text_edit)
        lyt.addWidget(self.pb_close, 0, Qt.AlignHCenter)
        self.setLayout(lyt)
        self.pb_close.clicked.connect(self.close)


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.all_data_model = list()
        self.frm_plot.setEnabled(False)
        self.frm_ctrl.setEnabled(False)
        self.frm_list.setEnabled(False)
        self.scan_id = None
        self.species_id = None
        self.line = None
        self.region = None

        #  import frame
        self.frm_open.sig_new_file.connect(self.slt_new_file)

        # list frame
        self.frm_list.sig_scan_id.connect(self.slt_new_scan)
        self.frm_list.sig_item_id.connect(self.slt_species)
        self.frm_list.sig_new_item.connect(self.slt_new_species)

        # plot frame
        self.frm_plot.sig_data_updated.connect(self.slt_update_data)
        self.frm_plot.sig_line_region_picked.connect(self.sig_line_region_picked)
        self.frm_plot.sig_set_enable.connect(self.slt_set_enable_list_ctrl)

        # control frame
        self.frm_ctrl.wg_gaus.sig_pick_params.connect(self.slt_pick_gauss_params)
        self.frm_ctrl.sig_add.connect(self.slt_add_species)
        self.frm_ctrl.sig_delete.connect(self.slt_delete_species)
        self.frm_ctrl.sig_update.connect(self.slt_update_species)
        self.frm_ctrl.wg_gaus.sig_set_enable.connect(self.slt_set_enable_list_plot)

        self.frm_list.pb_run.clicked.connect(self.slt_run)
        self.frm_open.pb_update.clicked.connect(self.slt_update_app)
        self.frm_list.pb_report.clicked.connect(self.slt_report)

    @Slot(object)
    def slt_new_file(self, all_data):
        self.all_data_model.clear()
        self.all_data_model = copy.deepcopy(all_data)
        self.frm_plot.setEnabled(True)
        # self.frm_ctrl.setEnabled(True)
        self.frm_list.setEnabled(True)
        self.frm_list.set_spin_box(len(self.all_data_model))

    @Slot(int)
    def slt_new_scan(self, scan_id: int):
        self.frm_ctrl.setEnabled(False)
        self.scan_id = scan_id
        self.frm_open.update_info(scan_id)
        data_model = self.all_data_model[self.scan_id]
        self.frm_plot.plot_data(data_model)
        self.frm_list.set_items(data_model.name_list)
        self.frm_ctrl.setEnabled(False)

    @Slot(int)
    def slt_species(self, func_id):
        self.species_id = func_id
        data_model = self.all_data_model[self.scan_id]
        self.frm_plot.plot_data(data_model, func_id)
        ts = self.get_turnoff_main(func_id)
        self.frm_ctrl.setup(data_model.next_index, data_model.model[func_id], turnoff_main=ts)
        self.frm_ctrl.setEnabled(True)

    @Slot()
    def slt_new_species(self):
        data_model = self.all_data_model[self.scan_id]
        self.frm_plot.plot_data(data_model)
        ts = self.get_turnoff_main()
        self.frm_ctrl.setup(data_model.next_index, turnoff_main=ts)
        self.frm_ctrl.setEnabled(True)

    @Slot(dms.DataModel)
    def slt_update_data(self):
        data = self.frm_plot.get_data()
        self.all_data_model[self.scan_id].data = data
        self.all_data_model[self.scan_id].clear_modeled()
        model = self.all_data_model[self.scan_id].model
        for i in range(len(model)):
            func = model[i]
            if func.type == dms.Types.EXP:
                func.exp.decay.value = None
                func.exp.amplitude.value = None
            elif func.type == dms.Types.GAUSS:
                func.gauss.amplitude.value = None
                func.gauss.sigma.value = None
        s = self.guess_model()
        if s:
            self.all_data_model[self.scan_id].reset_y_models()
        self.reset_list()

    @Slot()
    def sig_line_region_picked(self):
        self.line = self.frm_plot.get_line_value()
        self.region = self.frm_plot.get_region_values()
        self.frm_ctrl.wg_gaus.set_line(self.line)
        self.frm_ctrl.wg_gaus.set_region(self.region)

    @Slot(int, float, float, float)
    def slt_pick_gauss_params(self, state, center, value_1, value_2):
        self.frm_plot.pick_line_region_trim(state, center, value_1, value_2)

    @Slot()
    def slt_add_species(self):
        func = self.frm_ctrl.get_func()
        model = self.all_data_model[self.scan_id].model
        model.append(func)
        self.all_data_model[self.scan_id].set_model(model)
        self.all_data_model[self.scan_id].clear_modeled()
        s = self.guess_model()
        if s:
            self.all_data_model[self.scan_id].reset_y_models()
        self.reset_list()

    @Slot()
    def slt_delete_species(self):
        model = self.all_data_model[self.scan_id].model
        model.remove(model[self.species_id])
        self.all_data_model[self.scan_id].set_model(model)
        self.all_data_model[self.scan_id].clear_modeled()
        s = self.guess_model()
        if s:
            self.all_data_model[self.scan_id].reset_y_models()
        self.reset_list()

    @Slot()
    def slt_update_species(self):
        func = self.frm_ctrl.get_func()
        model = self.all_data_model[self.scan_id].model
        model[self.species_id] = func
        self.all_data_model[self.scan_id].set_model(model)
        self.all_data_model[self.scan_id].clear_modeled()
        s = self.guess_model()
        if s:
            self.all_data_model[self.scan_id].reset_y_models()
        self.reset_list()

    @Slot()
    def slt_run(self):
        self.setCursor(Qt.WaitCursor)
        fm = FitModel(self.all_data_model[self.scan_id])
        fm.init_fit()
        dm = fm.get_data_model()
        self.setCursor(Qt.ArrowCursor)
        self.all_data_model[self.scan_id] = dm
        self.reset_list()
        self.frm_list.lw_items.setCurrentRow(0)

    @Slot()
    def slt_update_app(self):
        app_path = os.path.dirname(os.path.abspath(__file__))
        py_exe = sys.executable
        setup_script = os.path.join(app_path, "setup_tools.py")
        p_1 = subprocess.run(['git', '-C', app_path, 'pull'], capture_output=True, text=True)
        p_2 = subprocess.run([py_exe, setup_script], capture_output=True, text=True)
        mess_box = UpdateBox()
        mess_box.text_edit.setText(p_1.stdout + "\n\n" + p_2.stdout)
        mess_box.exec()
        self.close()

    @Slot(bool)
    def slt_set_enable_list_ctrl(self, state):
        self.frm_open.setEnabled(state)
        self.frm_list.setEnabled(state)
        self.frm_ctrl.frm_left.setEnabled(state)
        self.frm_ctrl.stacked.setEnabled(state)

    @Slot(bool)
    def slt_set_enable_list_plot(self, state):
        self.frm_list.setEnabled(state)
        self.frm_plot.pb_region.setEnabled(state)
        self.frm_plot.pb_set_region.setEnabled(state)
        self.frm_open.setEnabled(state)

    @Slot()
    def slt_report(self):
        # checking
        data_model = self.all_data_model[self.scan_id]
        if data_model.data.y_model is None or data_model.data.residual is None:
            QMessageBox.warning(self, "warning!", "Fit a model, then try again!")
            return
        flag = True
        for i in range(len(data_model.model)):
            func = data_model.model[i]
            if not func.visible:
                continue
            if func.type == dms.Types.EXP:
                if func.exp.x is None or func.exp.y is None:
                    flag = False
                    break
            elif func.type == dms.Types.GAUSS:
                if func.gauss.x is None or func.gauss.y is None:
                    flag = False
                    break
        if not flag:
            QMessageBox.warning(self, "warning!", "Fit a model, then try again!")
            return

        home_dir = QDir.homePath()
        dialog_output = QFileDialog.getSaveFileName(self, "Report Results", home_dir, "(*.dat)")
        file_name = dialog_output[0]
        if len(file_name) == 0:
            return
        if not file_name.endswith(".dat"):
            file_name += ".dat"
        with open(file_name, 'w') as fid:
            fid.write(f"# Exponential Model : f(x) = A . e^[-x / Tau] , A: amplitude, Tau: decay\n")
            fid.write(f"# Gaussian Model : f(x) = (A / (Sigma . sqrt(2 . pi)) . ")
            fid.write(f"e ^ [-0.5 . (x - Mu)^2 / Sigma^2] , A: amplitude, Sigma: standard deviation, Mu: center\n#\n")
            area_raw = np.trapz(data_model.data.y_trim, data_model.data.x_trim)
            area_model = np.trapz(data_model.data.y_model, data_model.data.x_trim)
            rmsd = np.sqrt(np.mean(data_model.data.residual ** 2))
            for i in range(len(data_model.model)):
                func = data_model.model[i]
                # func = dms.Function()
                if not func.visible:
                    continue
                fid.write(f"# {func.name: <11s}: ")
                line = ''
                if func.type == dms.Types.EXP:
                    amp = func.exp.amplitude.value
                    dec = func.exp.decay.value
                    area = np.trapz(func.exp.y, func.exp.x)
                    line = f"A = {amp:>14.6e} ,   Tau = {dec:>14.6e} , " + " " * 14
                    line += f"Area = {area:>14.6e} , Ratio = {area / area_model * 100:>6.2f} %\n"
                elif func.type == dms.Types.GAUSS:
                    amp = func.gauss.amplitude.value
                    sig = func.gauss.sigma.value
                    cen = func.gauss.center.value
                    area = np.trapz(func.gauss.y, func.gauss.x)
                    line = f"A = {amp:>14.6e} , Sigma = {sig:>14.6e} , Mu = {cen:>6.3f} , "
                    line += f"Area = {area:>14.6e} , Ratio = {area / area_model * 100:>6.2f} %\n"
                fid.write(line)
            line = f"# Total Area of Raw Data     = {area_raw:>14.6e}\n"
            line += f"# Total Area of Modeled Data = {area_model:>14.6e}\n"
            line += f"# RMSD = {rmsd:.8f}\n#\n"
            fid.write(line)

    def reset_list(self):
        self.frm_list.set_items(self.all_data_model[self.scan_id].name_list)
        self.frm_ctrl.setEnabled(False)
        n = self.frm_list.lw_items.count() - 1
        self.frm_list.lw_items.setCurrentRow(n)

    def get_turnoff_main(self, func_id=None):
        data_model = self.all_data_model[self.scan_id]
        has_main = False
        for i in range(len(data_model.model)):
            func = data_model.model[i]
            if func.type == dms.Types.GAUSS:
                if func.gauss.main:
                    has_main = True
                    break
        is_main = False
        if func_id is not None:
            func = data_model.model[func_id]
            if func.type == dms.Types.GAUSS:
                if func.gauss.main:
                    is_main = True
        if has_main:
            if is_main:
                return False
            else:
                return True
        else:
            return False

    def guess_model(self):
        sigma_factor = 10
        data_model = self.all_data_model[self.scan_id]
        x = data_model.data.x_trim
        dx = np.mean(np.diff(x))
        y = data_model.data.y_trim
        ym = np.zeros(len(y))
        buffer = None
        # func = dms.Function()
        for i in range(len(data_model.model)):
            func = data_model.model[i]
            if func.type == dms.Types.EXP and func.visible:
                if func.exp.amplitude.value is None or func.exp.decay.value is None:
                    exp = lmfit.models.ExponentialModel(prefix='exp_')
                    params = exp.guess(y, x=x)
                    func.exp.decay.value = params.get('exp_decay').value
                    func.exp.amplitude.value = params.get('exp_amplitude').value
                buffer = copy.deepcopy(func)
                break

        if buffer is not None:
            # buffer = dms.Function()
            amp = buffer.exp.amplitude.value
            dec = buffer.exp.decay.value
            ym += dms.Exponential.get_fx(x, amp, dec)

        y_r = y - ym

        # find main peak
        main_peak = None
        for i in range(len(data_model.model)):
            func = data_model.model[i]
            # func = dms.Function()
            if func.type == dms.Types.GAUSS and func.visible and func.gauss.main:
                cent = func.gauss.center.value
                amp = func.gauss.amplitude.value
                sig = func.gauss.sigma.value
                if amp is None or sig is None:
                    y_cent = y_r[np.argmin(np.abs(x - cent))]
                    sig = dx * sigma_factor
                    amp = y_cent * sig * np.sqrt(2 * np.pi)
                    amp = max(1e-4, abs(amp))
                    func.gauss.sigma.value = sig
                    func.gauss.amplitude.value = amp
                # ym += dms.Gaussian.get_fx(x, amplitude=amp, sigma=sig, center=cent)
                # y_r = y - ym
                main_peak = copy.deepcopy(func)
                break
        # check bound and main peaks
        for i in range(len(data_model.model)):
            func = data_model.model[i]
            # func = dms.Function()
            if func.type == dms.Types.GAUSS and func.visible and not func.gauss.main:
                bound = func.gauss.sigma.bound
                if bound and main_peak is None:
                    QMessageBox.warning(self, "warning", "Set a species as the main one!")
                    return False

        # guess other peaks
        for i in range(len(data_model.model)):
            func = data_model.model[i]
            # func = dms.Function()
            if func.type == dms.Types.GAUSS and func.visible and not func.gauss.main:
                cent = func.gauss.center.value
                amp = func.gauss.amplitude.value
                sig = func.gauss.sigma.value
                bound = func.gauss.sigma.bound
                if bound:
                    sig_main = main_peak.gauss.sigma.value
                    if amp is None or sig is None or sig != sig_main:
                        sig = sig_main
                        func.gauss.sigma.value = sig
                        if amp is None:
                            y_cent = y_r[np.argmin(np.abs(x - cent))]
                            amp = y_cent * sig * np.sqrt(2 * np.pi)
                            amp = max(1e-4, abs(amp))
                            func.gauss.amplitude.value = amp
                else:
                    if amp is None or sig is None:
                        y_cent = y_r[np.argmin(np.abs(x - cent))]
                        sig = dx * sigma_factor
                        amp = y_cent * sig * np.sqrt(2 * np.pi)
                        amp = max(1e-4, abs(amp))
                        func.gauss.sigma.value = sig
                        func.gauss.amplitude.value = amp
                # ym += dms.Gaussian.get_fx(x, amplitude=amp, sigma=sig, center=cent)
                # y_r = y - ym
        return True
