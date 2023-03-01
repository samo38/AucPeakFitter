from PySide6 import (QtWidgets, QtCore, QtGui)
from PySide6.QtCore import (Slot, Signal)
from gui_main_window import Ui_MainWindow
import data_models as dms


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
        # self.pb_set_reg.setEnabled(False)
        self.frm_list.lw_species.clear()

        # self.frm_open.sig_new_file.connect(self.slt_new_file)
        # self.frm_list.spin_box.valueChanged.connect(self.slt_new_scan)
        # self.wg_plot.sig_data_models_updated.connect(self.slt_update_data_models)
        # self.frm_list.lw_species.currentRowChanged.connect(self.slt_model_changed)
        # self.frm_ctrl.sig_pick_line.connect(self.slt_pick_line_trim)

    @Slot(object)
    def slt_new_file(self, all_data):
        self.all_data_models = all_data
        self.frm_plot.setEnabled(True)
        self.frm_ctrl.setEnabled(True)
        self.frm_list.setEnabled(True)
        self.set_scan_spb()

    @Slot(int)
    def slt_new_scan(self, scan_id: int):
        scan_id -= 1
        self.scan_id = scan_id
        self.frm_open.update_info(scan_id)
        data_model = dms.DataModels
        # model = self.all_data_models[self.scan_id]
        # self.wg_plot.import_model(self.all_data_models[])
        self.set_lw_species()

    @Slot(dms.DataModels)
    def slt_update_data_models(self, model):
        self.all_data_models[self.scan_id] = model

    @Slot(int)
    def slt_model_changed(self, row):
        return
        # if self.frm_list.lw_species.currentTextChanged() == ":: New Species":
        #     # self.setup_new_species()
        #
        #     print()

    @Slot(int, float)
    def slt_pick_line_trim(self, state, value):
        self.wg_plot.pick_line_trim(state, value)
        if state == 0:
            self.frm_ctrl.lined_picked = self.wg_plot.line_val_trim

    def set_scan_spb(self):
        self.frm_list.spin_box.valueChanged.disconnect(self.slt_new_scan)
        self.frm_list.spin_box.clear()
        self.frm_list.spin_box.setMinimum(1)
        self.frm_list.spin_box.setMaximum(self.n_scans)
        self.frm_list.spin_box.valueChanged.connect(self.slt_new_scan)
        self.frm_list.spin_box.setValue(self.n_scans)

    def set_lw_species(self):
        self.frm_list.lw_species.currentRowChanged.disconnect(self.slt_model_changed)
        self.frm_list.lw_species.clear()
        data_models = self.all_data_models[self.scan_id]
        n_models = len(data_models.models)
        for i in range(n_models):
            name = f"{i + 1}-{data_models.models[i].name}-"
            name += f"{data_models.models[i].type.lower()}"
            if data_models.models[i].type == "GAUSS":
                if data_models.models[i].params.sigma.bound:
                    name += "-B"
            self.frm_list.lw_species.addItem(name)
        self.frm_list.lw_species.addItem(":: New Species")
        self.frm_list.lw_species.currentRowChanged.connect(self.slt_model_changed)
        self.model_id = 0
        self.frm_list.lw_species.setCurrentRow(self.model_id)





