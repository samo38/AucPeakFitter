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
import numpy as np
from auc_data_io import AucRawData
import gui_import
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
            data = dms.Data()
            data.set_raw(x_values, y_values[i])
            data.set_trim(x_values, y_values[i])
            data_models = dms.DataModel()
            data_models.data = data
            all_data_models.append(data_models)
        self.sig_new_file.emit(all_data_models)

    def update_info(self, n: int):
        rpm = self.rpm[n] / 1000
        self.le_rpm.setText(f"{rpm: g}k")
        wave = self.wavelength[n]
        self.le_wavl.setText(f"{wave: g}")
        temp = self.temperature[n]
        self.le_temp.setText(f"{temp: g}")


