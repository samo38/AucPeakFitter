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

