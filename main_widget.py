from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QDir,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy, QFileDialog, QMessageBox,
    QSpinBox, QVBoxLayout, QWidget, QMainWindow)
from PySide6.QtCore import (Slot, Signal)
import numpy as np
import copy
from gui_main_window import Ui_MainWindow
import data_models as dms
from fit_model import FitModel


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
        self.frm_ctrl.sig_add.connect(self.slt_add_species)
        self.frm_ctrl.sig_delete.connect(self.slt_delete_species)
        self.frm_ctrl.sig_update.connect(self.slt_update_species)

        self.frm_list.pb_run.clicked.connect(self.slt_run)

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
        self.frm_plot.set_data(data_model.data)
        sp_list = self.__get_sp_list()
        self.frm_list.set_items(sp_list)

    @Slot(int)
    def slt_setup_species(self, func_id):
        self.species_id = func_id
        data_model = self.all_data_model[self.scan_id]
        x_arr = data_model.data.x_trim
        self.frm_ctrl.setup(x_arr, data_model.next_index, data_model.model[func_id])
        self.frm_ctrl.setEnabled(True)

    @Slot()
    def slt_setup_new_species(self):
        data_model = self.all_data_model[self.scan_id]
        x_arr = data_model.data.x_trim
        self.frm_ctrl.setup(x_arr, data_model.next_index)
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

    @Slot(int, float)
    def slt_pick_line(self, state, value):
        self.frm_plot.pick_line_trim(state, value)

    @Slot(int, float, float)
    def slt_pick_region(self, state, value_1, value_2):
        self.frm_plot.pick_region_trim(state, value_1, value_2)

    @Slot()
    def slt_add_species(self):
        func = self.frm_ctrl.get_func()
        model = self.all_data_model[self.scan_id].model
        model.append(func)
        self.__reset_sp_list()

    @Slot()
    def slt_delete_species(self):
        model = self.all_data_model[self.scan_id].model
        model.remove(model[self.species_id])
        self.__reset_sp_list()

    @Slot()
    def slt_update_species(self):
        func = self.frm_ctrl.get_func()
        model = self.all_data_model[self.scan_id].model
        model[self.species_id] = func
        self.__reset_sp_list()

    @Slot()
    def slt_run(self):
        fm = FitModel(self.all_data_model[self.scan_id])
        fm.eval_components()
        dm = fm.get_data_model()
        self.all_data_model[self.scan_id] = dm
        self.frm_plot.set_data(dm.get_data())

    def __get_sp_list(self):
        data_model = self.all_data_model[self.scan_id]
        sp_list = []
        n_sp = len(data_model.model)
        for i in range(n_sp):
            name = f"{data_model.model[i].name}"
            if data_model.model[i].type == dms.Types.GAUSS:
                if data_model.model[i].gauss.sigma.bound is True:
                    name += " - bound"
            sp_list.append(name)
        sp_list.append(":::::: New Species ::::::")
        return sp_list

    def __check_all_functions(self):
        data_model = self.all_data_model[self.scan_id]
        model = copy.deepcopy(data_model.model)
        model_out = []
        buffer_state = False
        buffer = None
        idx = 1
        for i in range(len(model)):
            # func = dms.Function(dms.Types.GAUSS)
            func = model[i]
            if func.type == dms.Types.EXP:
                if not buffer_state:
                    buffer = copy.deepcopy(func)
                    if buffer.visible:
                        buffer.name = "Buffer"
                    else:
                        buffer.name = "**Buffer**"
                    buffer_state = True
                else:
                    QMessageBox.warning(self, "Warning!", "A buffer species is already set!")
            elif func.type == dms.Types.GAUSS:
                tf = copy.deepcopy(func)
                if tf.visible:
                    tf.name = f"Species {idx}"
                else:
                    tf.name = f"**Species {idx}**"
                idx += 1
                model_out.append(tf)
        if buffer is not None:
            model_out = [buffer] + model_out
        data_model.next_index = idx
        data_model.optimized = False
        data_model.model = model_out

    def __reset_sp_list(self):
        self.__check_all_functions()
        sp_list = self.__get_sp_list()
        self.frm_list.set_items(sp_list)
        self.frm_ctrl.setEnabled(False)

