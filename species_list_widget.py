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
import gui_species_list


class SpeciesList(QFrame, gui_species_list.Ui_Frame):

    sig_scan_id = Signal(int)
    sig_new_item = Signal()
    sig_item_id = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.sb_scans.valueChanged.connect(self.slt_scan_id)
        self.lw_items.currentRowChanged.connect(self.slt_item_changed)

    @Slot(int)
    def slt_scan_id(self, n: int):
        self.sig_scan_id.emit(n - 1)

    @Slot(int)
    def slt_item_changed(self, row):
        n_items = self.lw_items.count()
        if row == (n_items - 1):
            self.sig_new_item.emit()
        else:
            self.sig_item_id.emit(row)

    def set_spin_box(self, n: int):
        self.sb_scans.valueChanged.disconnect(self.slt_scan_id)
        self.sb_scans.clear()
        self.sb_scans.setMinimum(1)
        self.sb_scans.setMaximum(n)
        self.sb_scans.valueChanged.connect(self.slt_scan_id)
        self.sb_scans.setValue(n)

    def set_items(self, items: list):
        self.lw_items.currentRowChanged.disconnect(self.slt_item_changed)
        self.lw_items.clear()
        for i in range(len(items)):
            self.lw_items.addItem(items[i])
        self.lw_items.currentRowChanged.connect(self.slt_item_changed)

