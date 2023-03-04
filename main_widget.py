from PySide6 import (QtWidgets, QtCore, QtGui)
from PySide6.QtCore import (Slot, Signal)
from gui_main_window import Ui_MainWindow
import data_models as dms


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    # sig_pick_region = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.all_data_model = None
        self.frm_plot.setEnabled(False)
        self.frm_ctrl.setEnabled(False)
        self.frm_list.setEnabled(False)
        self.scan_id = None
        self.species_id = None
        self.line = None
        self.region = None
        # self.pb_set_reg.setEnabled(False)

        #  import frame
        self.frm_open.sig_new_file.connect(self.slt_new_file)

        # list frame
        self.frm_list.sig_scan_id.connect(self.slt_new_scan)
        self.frm_list.sig_item_id.connect(self.slt_setup_species)
        self.frm_list.sig_new_item.connect(self.slt_setup_new_species)

        # plot frame
        self.frm_plot.sig_data_updated.connect(self.slt_update_data)
        self.frm_plot.sig_line_picked.connect(self.slt_line_picked)
        self.frm_plot.sig_region_picked.connect(self.slt_region_picked)

        # control frame
        self.frm_ctrl.wg_gaus.sig_pick_line.connect(self.slt_pick_line)
        self.frm_ctrl.wg_gaus.sig_pick_region.connect(self.slt_pick_region)
        # self.frm_ctrl.sig_pick_line.connect(self.slt_pick_line_trim)




    @Slot(object)
    def slt_new_file(self, all_data):
        self.all_data_model = all_data
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
        data = data_model.get_data()
        self.frm_plot.set_data(data)
        sp_list = self.__get_sp_list()
        self.frm_list.set_items(sp_list)

    @Slot(int)
    def slt_setup_species(self, m_id):
        func = self.all_data_model[self.scan_id].model[m_id]
        x_arr = self.all_data_model[self.scan_id].data.x_trim
        n = self.frm_list.lw_items.count()
        self.frm_ctrl.setup(x_arr, n, func)
        self.frm_ctrl.setEnabled(True)

    @Slot()
    def slt_setup_new_species(self):
        x_arr = self.all_data_model[self.scan_id].data.x_trim
        n = self.frm_list.lw_items.count()
        self.frm_ctrl.setup(x_arr, n)
        self.frm_ctrl.setEnabled(True)

    @Slot(dms.DataModel)
    def slt_update_data(self):
        data = self.frm_plot.get_data()
        self.all_data_model[self.scan_id].data = data

    @Slot()
    def slt_line_picked(self):
        self.line = self.frm_plot.get_line_value()
        self.frm_ctrl.wg_gaus.set_line(self.line)

    @Slot()
    def slt_region_picked(self):
        self.region = self.frm_plot.get_region_values()
        self.frm_ctrl.wg_gaus.set_region(self.region)

    @Slot(int)
    def slt_model_changed(self, row):
        return
        # if self.frm_list.lw_species.currentTextChanged() == ":: New Species":
        #     # self.setup_new_species()
        #
        #     print()

    @Slot(int, float)
    def slt_pick_line(self, state, value):
        self.frm_plot.pick_line_trim(state, value)

    @Slot(int, float, float)
    def slt_pick_region(self, state, value_1, value_2):
        self.frm_plot.pick_region_trim(state, value_1, value_2)

    def __get_sp_list(self):
        data_model = self.all_data_model[self.scan_id]
        sp_list = []
        n_sp = len(data_model.model)
        for i in range(n_sp):
            name = f"{i + 1}-{data_model.model[i].name}-"
            name += f"{data_model.model[i].type.lower()}"
            if data_model.model[i].type == "GAUSS":
                if data_model.model[i].params.sigma.bound:
                    name += "-B"
            sp_list.append(name)
        sp_list.append("::: New Species")
        return sp_list


