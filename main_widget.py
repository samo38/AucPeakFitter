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
        self.frm_plot.sig_line_picked.connect(self.slt_line_picked)
        self.frm_plot.sig_region_picked.connect(self.slt_region_picked)
        self.frm_plot.sig_set_enable.connect(self.slt_set_enable_list_ctrl)

        # control frame
        self.frm_ctrl.wg_gaus.sig_pick_line.connect(self.slt_pick_line)
        self.frm_ctrl.wg_gaus.sig_pick_region.connect(self.slt_pick_region)
        self.frm_ctrl.sig_add.connect(self.slt_add_species)
        self.frm_ctrl.sig_delete.connect(self.slt_delete_species)
        self.frm_ctrl.sig_update.connect(self.slt_update_species)
        self.frm_ctrl.wg_gaus.sig_set_enable.connect(self.slt_set_enable_list_plot)

        self.frm_list.pb_run.clicked.connect(self.slt_run)
        self.frm_open.pb_update.clicked.connect(self.slt_update_app)

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
        self.frm_ctrl.setup(data_model.next_index, data_model.model[func_id])
        self.frm_ctrl.setEnabled(True)

    @Slot()
    def slt_new_species(self):
        data_model = self.all_data_model[self.scan_id]
        self.frm_plot.plot_data(data_model)
        self.frm_ctrl.setup(data_model.next_index)
        self.frm_ctrl.setEnabled(True)

    @Slot(dms.DataModel)
    def slt_update_data(self):
        data = self.frm_plot.get_data()
        self.all_data_model[self.scan_id].data = data
        self.all_data_model[self.scan_id].clear_modeled()
        self._reset_list()

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
        self.all_data_model[self.scan_id].set_model(model)
        self.all_data_model[self.scan_id].clear_modeled()
        self._reset_list()

    @Slot()
    def slt_delete_species(self):
        model = self.all_data_model[self.scan_id].model
        model.remove(model[self.species_id])
        self.all_data_model[self.scan_id].set_model(model)
        self.all_data_model[self.scan_id].clear_modeled()
        self._reset_list()

    @Slot()
    def slt_update_species(self):
        func = self.frm_ctrl.get_func()
        model = self.all_data_model[self.scan_id].model
        model[self.species_id] = func
        self.all_data_model[self.scan_id].set_model(model)
        self.all_data_model[self.scan_id].clear_modeled()
        self._reset_list()

    @Slot()
    def slt_run(self):
        self.setCursor(Qt.WaitCursor)
        fm = FitModel(self.all_data_model[self.scan_id])
        fm.init_fit()
        dm = fm.get_data_model()
        self.setCursor(Qt.ArrowCursor)
        self.all_data_model[self.scan_id] = dm
        self._reset_list()
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

    def _reset_list(self):
        self.frm_list.set_items(self.all_data_model[self.scan_id].name_list)
        self.frm_ctrl.setEnabled(False)
        n = self.frm_list.lw_items.count() - 1
        self.frm_list.lw_items.setCurrentRow(n)

