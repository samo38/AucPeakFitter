from PySide6 import (QtWidgets, QtCore, QtGui)
from PySide6.QtCore import (Slot, Signal)
from gui_main_window import Ui_MainWindow
from auc_data_io import AucRawData
import data_models as dm


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    # sig_pick_region = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.all_data_models = None
        self.n_scans = None
        self.temperature = None
        self.rpm = None
        self.wavelength = None
        self.frm_plot.setEnabled(False)
        self.frm_ctrl.setEnabled(False)
        self.frm_list.setEnabled(False)
        self.scan_id = None
        self.model_id = None
        self.pb_set_reg.setEnabled(False)

        self.frm_ctrl.cmb_type.clear()
        self.frm_ctrl.cmb_type.addItem("Gaussian")
        self.frm_ctrl.cmb_type.addItem("Exponential")
        self.frm_ctrl.cmb_type.setCurrentIndex(0)
        self.frm_ctrl.stacked.setCurrentWidget(self.frm_ctrl.wg_gaus)

        self.frm_open.pb_open.clicked.connect(self.slt_import)
        self.frm_list.spin_box.valueChanged.connect(self.slt_new_scan)
        self.pb_reg.clicked.connect(self.reg_clicked)
        self.pb_set_reg.clicked.connect(self.set_clicked)
        self.wg_plot.sig_data_models_updated.connect(self.slt_update_data_models)
        self.frm_list.lw_list.currentRowChanged.connect(self.slt_model_updated)
        self.frm_ctrl.cmb_type.currentTextChanged.connect(self.slt_func_updated)

    @Slot(object)
    def slt_import(self):
        home_dir = QtCore.QDir.homePath()
        dialog_output = QtWidgets.QFileDialog.getOpenFileName(self, "Open AUC File",
                                                              home_dir, "(*.auc)")
        file_name = dialog_output[0]
        if len(file_name) == 0:
            return
        auc_data = AucRawData()
        state = auc_data.read(file_name)
        if not state:
            QtWidgets.QMessageBox.warning(self, "Warning!",
                                          f"The following file is not readable by this program:\n{file_name}")
            return
        self.frm_open.le_desc.setText(auc_data.description)
        self.frm_open.le_type.setText(auc_data.type)
        self.frm_open.le_cell.setText(str(auc_data.cell))
        self.frm_open.le_chan.setText(auc_data.channel)
        self.n_scans = len(auc_data.rvalues)
        self.temperature = auc_data.temperature
        self.rpm = auc_data.rpm
        self.wavelength = auc_data.wavelength
        x_values = auc_data.xvalues
        y_values = auc_data.rvalues
        self.all_data_models = []
        for i in range(self.n_scans):
            data_models = dm.DataModels()
            data_models.set_raw(x_values, y_values[i])
            data_models.set_trim(x_values, y_values[i])
            self.all_data_models.append(data_models)
        self.frm_plot.setEnabled(True)
        self.frm_ctrl.setEnabled(True)
        self.frm_list.setEnabled(True)
        self.set_scan_spb()

    @Slot(int)
    def slt_new_scan(self, scan_id: int):
        scan_id -= 1
        self.scan_id = scan_id
        rpm = self.rpm[scan_id] / 1000
        self.frm_open.le_rpm.setText(f"{rpm: g}k")
        wave = self.wavelength[scan_id]
        self.frm_open.le_wavl.setText(f"{wave: g}")
        temp = self.temperature[scan_id]
        self.frm_open.le_temp.setText(f"{temp: g}")
        self.wg_plot.import_model(self.all_data_models[self.scan_id])
        self.set_lw_species()

    @Slot(bool)
    def reg_clicked(self, checked):
        icon1 = QtGui.QIcon()
        icon2 = QtGui.QIcon()
        icon1.addFile(u":/Icon/Resources/Icons/horizontal_distribute_FILL0_wght400_GRAD0_opsz48.svg", QtCore.QSize(),
                      QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addFile(u":/Icon/Resources/Icons/cancel_FILL0_wght400_GRAD0_opsz48.svg", QtCore.QSize(),
                      QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # self.pb_reg.setIconSize(QSize(16, 16))
        if checked:
            self.pb_reg.setText("Cancel")
            self.pb_reg.setIcon(icon2)
            self.pb_reg.setStyleSheet(u"background-color: rgb(246, 97, 81);")
            self.pb_set_reg.setStyleSheet(u"background-color: rgb(143, 240, 164);")
            self.pb_set_reg.setEnabled(True)
            self.wg_plot.pick_region_raw(1)
        else:
            self.pb_reg.setText("Region")
            self.pb_reg.setIcon(icon1)
            self.pb_reg.setStyleSheet(u"background-color: rgb(249, 240, 107);")
            self.pb_set_reg.setStyleSheet(u"background-color: ;")
            self.pb_set_reg.setEnabled(False)
            self.wg_plot.pick_region_raw(-1)

    @Slot()
    def set_clicked(self):
        icon = QtGui.QIcon()
        icon.addFile(u":/Icon/Resources/Icons/horizontal_distribute_FILL0_wght400_GRAD0_opsz48.svg", QtCore.QSize(),
                     QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_reg.setText("Region")
        self.pb_reg.setChecked(False)
        self.pb_reg.setIcon(icon)
        self.pb_reg.setStyleSheet(u"background-color: rgb(249, 240, 107);")
        self.pb_set_reg.setStyleSheet(u"background-color: ;")
        self.pb_set_reg.setEnabled(False)
        self.wg_plot.pick_region_raw(0)

    @Slot(dm.DataModels)
    def slt_update_data_models(self, model):
        self.all_data_models[self.scan_id] = model

    @Slot(int)
    def slt_model_updated(self, row):
        print()

    @Slot(str)
    def slt_func_updated(self, text):
        if text == 'Gaussian':
            self.frm_ctrl.stacked.setCurrentWidget(self.frm_ctrl.wg_gaus)
        elif text == 'Exponential':
            self.frm_ctrl.stacked.setCurrentWidget(self.frm_ctrl.wg_exp)

    def set_scan_spb(self):
        self.frm_list.spin_box.valueChanged.disconnect(self.slt_new_scan)
        self.frm_list.spin_box.clear()
        self.frm_list.spin_box.setMinimum(1)
        self.frm_list.spin_box.setMaximum(self.n_scans)
        self.frm_list.spin_box.valueChanged.connect(self.slt_new_scan)
        self.frm_list.spin_box.setValue(self.n_scans)

    def set_lw_species(self):
        self.frm_list.lw_list.currentRowChanged.disconnect(self.slt_model_updated)
        self.frm_list.lw_list.clear()
        data_models = self.all_data_models[self.scan_id]
        n_models = len(data_models.models)
        for i in range(n_models):
            name = f"{i + 1}-{data_models.models[i].name}-"
            name += f"{data_models.models[i].type.lower()}"
            if data_models.models[i].type == "GAUSS":
                if data_models.models[i].params.sigma.bound:
                    name += "-B"
            self.frm_list.lw_list.addItem(name)
        self.frm_list.lw_list.currentRowChanged.connect(self.slt_model_updated)
        self.model_id = 0

