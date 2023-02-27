from PySide6 import (QtWidgets, QtCore)
from PySide6.QtCore import (Slot, Signal)
from gui_main_window import Ui_MainWindow
from AucDataIO import AucRawData


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    # sig_new_scan = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.auc_data = None
        self.n_scans = None
        self.x_values = None
        self.y_values = None
        self.temperature = None
        self.rpm = None
        self.wavelength = None
        self.frm_plot.setEnabled(False)
        self.frm_ctrl.setEnabled(False)
        self.frm_list.setEnabled(False)
        self.scan_id = None

        self.frm_open.pb_open.clicked.connect(self.slt_import)
        self.frm_list.spin_box.valueChanged.connect(self.slt_new_scan)

    @Slot(object)
    def slt_import(self):
        home_dir = QtCore.QDir.homePath()
        dialog_output = QtWidgets.QFileDialog.getOpenFileName(self, "Open AUC File",
                                                              home_dir, "(*.auc)")
        file_name = dialog_output[0]
        if len(file_name) == 0:
            return
        self.auc_data = AucRawData()
        self.auc_data.read(file_name)
        self.frm_open.le_desc.setText(self.auc_data.description)
        self.frm_open.le_type.setText(self.auc_data.type)
        self.frm_open.le_cell.setText(str(self.auc_data.cell))
        self.frm_open.le_chan.setText(self.auc_data.channel)
        self.n_scans = len(self.auc_data.rvalues)
        self.x_values = self.auc_data.xvalues
        self.y_values = self.auc_data.rvalues
        self.temperature = self.auc_data.temperature
        self.rpm = self.auc_data.rpm
        self.wavelength = self.auc_data.wavelength
        self.frm_plot.setEnabled(True)
        self.frm_ctrl.setEnabled(True)
        self.frm_list.setEnabled(True)
        self.set_scan_spb()

    @Slot(int)
    def slt_new_scan(self, scan_id: int):
        scan_id -= 1
        self.scan_id = scan_id
        rpm = self.rpm[scan_id] / 1000
        self.frm_open.le_rpm.setText(f"{rpm: g} k")
        wave = self.wavelength[scan_id]
        self.frm_open.le_wavl.setText(f"{wave: g}")
        temp = self.temperature[scan_id]
        self.frm_open.le_temp.setText(f"{temp: g}")

        # self.frm_open.le_rpm.setText(self.auc_data.rpm)
        # self.frm_open.le_rpm.setText(self.auc_data.temperature)

    def set_scan_spb(self):
        self.frm_list.spin_box.valueChanged.disconnect(self.slt_new_scan)
        self.frm_list.spin_box.clear()
        self.frm_list.spin_box.setMinimum(1)
        self.frm_list.spin_box.setMaximum(self.n_scans)

        self.frm_list.spin_box.valueChanged.connect(self.slt_new_scan)
        self.frm_list.spin_box.setValue(self.n_scans)

