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
import gui_species_list


class SpeciesList(QFrame, gui_species_list.Ui_Frame):

    sig_scan_id = Signal(int)
    sig_new_item = Signal()
    sig_item_id = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.flag_row = False
        self.flag_click = False
        self.new_sp_str = ":::::::::: New Species ::::::::::"
        self.sb_scans.valueChanged.connect(self.slt_scan_id)
        self.lw_items.itemClicked.connect(self.slt_item_clicked)
        self.lw_items.currentRowChanged.connect(self.slt_row_changed)

    @Slot(int)
    def slt_scan_id(self, n: int):
        self.sig_scan_id.emit(n - 1)

    @Slot(QListWidgetItem)
    def slt_item_clicked(self, item):
        if self.flag_row:
            self.flag_row = False
            return
        row = self.lw_items.currentRow()
        self.flag_click = True
        self.select_row(row)

    @Slot(int)
    def slt_row_changed(self, row):
        if self.flag_click:
            self.flag_click = False
            return
        self.flag_row = True
        self.select_row(row)

    def set_spin_box(self, n: int):
        self.sb_scans.valueChanged.disconnect(self.slt_scan_id)
        self.sb_scans.clear()
        self.sb_scans.setMinimum(1)
        self.sb_scans.setMaximum(n)
        self.sb_scans.valueChanged.connect(self.slt_scan_id)
        self.sb_scans.setValue(n)

    def set_items(self, items: list):
        self.lw_items.itemClicked.disconnect(self.slt_item_clicked)
        self.lw_items.currentRowChanged.disconnect(self.slt_row_changed)
        self.lw_items.clear()
        for i in range(len(items)):
            self.lw_items.addItem(items[i])
        self.lw_items.addItem(self.new_sp_str)
        self.lw_items.itemClicked.connect(self.slt_item_clicked)
        self.lw_items.currentRowChanged.connect(self.slt_row_changed)

    def select_row(self, row):
        self.lw_items.currentRowChanged.disconnect(self.slt_row_changed)
        self.lw_items.setCurrentRow(row)
        self.lw_items.currentRowChanged.connect(self.slt_row_changed)
        item = self.lw_items.item(row)
        if "New Species" in item.text():
            self.sig_new_item.emit()
        else:
            self.sig_item_id.emit(row)
