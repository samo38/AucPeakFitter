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


class PlotWidget(QFrame):

    sig_data_updated = Signal()
    sig_line_picked = Signal()
    sig_region_picked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(1)

        self.x_raw = None
        self.y_raw = None
        self.x_trim = None
        self.y_trim = None
        self.region_values = None
        self.line_value = None

        plt_win = pyqtgraph.GraphicsLayoutWidget()
        self.plt_species = plt_win.addPlot(title="Trimmed & Decomposed")  # PlotItem
        self.plt_import = plt_win.addPlot(title="Imported")
        plt_win.nextRow()
        self.plt_error = plt_win.addPlot(title="Residuals")
        self.plt_model = plt_win.addPlot(title="Trimmed & Modeled")

        self.icon_check = QIcon()
        self.icon_check.addFile(u":/Icon/Resources/Icons/check_circle_FILL0_wght400_GRAD0_opsz48.svg",
                                     QSize(), QIcon.Normal, QIcon.Off)
        self.icon_region = QIcon()
        self.icon_region.addFile(u":/Icon/Resources/Icons/horizontal_distribute_FILL0_wght400_GRAD0_opsz48.svg",
                                     QSize(), QIcon.Normal, QIcon.Off)
        self.icon_cancel = QIcon()
        self.icon_cancel.addFile(u":/Icon/Resources/Icons/cancel_FILL0_wght400_GRAD0_opsz48.svg",
                                 QSize(), QIcon.Normal, QIcon.Off)

        self.pb_region = QPushButton(u"Region")
        self.pb_region.setCheckable(True)
        self.pb_region.setIcon(self.icon_region)
        self.pb_region.setStyleSheet(u"background-color: rgb(249, 240, 107);")
        self.pb_region.setIconSize(QSize(16, 16))

        self.pb_set_region = QPushButton("Apply")
        self.pb_set_region.setEnabled(False)
        self.pb_set_region.setIcon(self.icon_check)
        self.pb_set_region.setIconSize(QSize(16, 16))

        lyt_pb = QVBoxLayout()
        lyt_pb.setContentsMargins(0, 0, 0, 0)
        lyt_pb.setSpacing(1)
        lyt_pb.addWidget(self.pb_region)
        lyt_pb.addWidget(self.pb_set_region)
        lyt_pb.addStretch(1)

        self.curve_import = self.plt_import.plot(pen='y')  # PlotDataItem
        self.curve_trim = self.plt_species.plot(pen='y')
        self.curve_species = []
        self.curve_residue = self.plt_error.plot(pen='g')
        self.curve_model_data = self.plt_model.plot(pen='y')
        self.curve_model_fit = self.plt_model.plot(pen='r')

        self.region_picker_import = pyqtgraph.LinearRegionItem(pen="white")
        self.region_picker_trim = pyqtgraph.LinearRegionItem(pen="white")
        self.line_picker_trim = pyqtgraph.InfiniteLine(pen="white", movable=True)
        # self.picker_raw.setZValue(-10)

        layout = QHBoxLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.addWidget(plt_win)
        layout.addLayout(lyt_pb)
        self.setLayout(layout)

        self.region_picker_import.sigRegionChanged.connect(self.update_trim)
        self.pb_region.clicked.connect(self.update_region)
        self.pb_set_region.clicked.connect(self.set_region)

    @Slot(object)
    def update_trim(self):
        [min_val, max_val] = self.region_picker_import.getRegion()
        ind = np.logical_and(self.x_raw >= min_val, self.x_raw <= max_val)
        x_temp = self.x_raw[ind]
        y_temp = self.y_raw[ind]
        self.plot_trim(x_temp, y_temp)

    @Slot(bool)
    def update_region(self, checked):
        # self.pb_reg.setIconSize(QSize(16, 16))
        if checked:
            self.pb_region.setText("Cancel")
            self.pb_region.setIcon(self.icon_cancel)
            self.pb_region.setStyleSheet(u"background-color: rgb(246, 97, 81);")
            self.pb_set_region.setStyleSheet(u"background-color: rgb(143, 240, 164);")
            self.pb_set_region.setEnabled(True)
            self.pick_region_import(1)
        else:
            self.pb_region.setText("Region")
            self.pb_region.setIcon(self.icon_region)
            self.pb_region.setStyleSheet(u"background-color: rgb(249, 240, 107);")
            self.pb_set_region.setStyleSheet(u"background-color: ;")
            self.pb_set_region.setEnabled(False)
            self.pick_region_import(-1)

    @Slot()
    def set_region(self):
        self.pb_region.setText("Region")
        self.pb_region.setChecked(False)
        self.pb_region.setIcon(self.icon_region)
        self.pb_region.setStyleSheet(u"background-color: rgb(249, 240, 107);")
        self.pb_set_region.setStyleSheet(u"background-color: ;")
        self.pb_set_region.setEnabled(False)
        self.pick_region_import(0)

    def set_data(self, x_raw: np.array, y_raw: np.array, x_trim: np.array, y_trim: np.array):
        self.x_raw = x_raw
        self.y_raw = y_raw
        self.x_trim = x_trim
        self.y_trim = y_trim
        self.plot_raw()
        self.plot_trim()

    def get_data(self):
        return self.x_raw, self.y_raw, self.x_trim, self.y_trim

    def plot_raw(self):
        self.curve_import.setData(self.x_raw, self.y_raw)

    def plot_trim(self, x=None, y=None):
        if (x is not None) and (y is not None):
            self.curve_trim.setData(x, y)
        else:
            self.curve_trim.setData(self.x_trim, self.y_trim)

    def pick_region_import(self, state: int):
        if state == 1:  # connect picker
            self.region_picker_import.setRegion([np.min(self.x_trim), np.max(self.x_trim)])
            self.plt_import.addItem(self.region_picker_import)
        elif state == -1:  # cancel and close piker
            self.plt_import.removeItem(self.region_picker_import)
            self.plot_trim()
        elif state == 0:  # accept and close picker
            data = self.curve_trim.getData()
            self.x_trim = data[0]
            self.y_trim = data[1]
            self.plt_import.removeItem(self.region_picker_import)
            self.sig_data_updated.emit()

    def pick_region_trim(self, state: int, x1: float, x2: float):
        if state == 1:  # connect picker
            self.region_picker_trim.setRegion([x1, x2])
            self.plt_species.addItem(self.region_picker_trim)
        elif state == 0:  # accept and close picker
            self.region_values = self.region_picker_trim.getRegion()
            self.plt_species.removeItem(self.region_picker_trim)
            self.sig_region_picked.emit()

    def pick_line_trim(self, state: int, value: float):
        if state == 1:
            self.line_picker_trim.setValue(value)
            self.plt_species.addItem(self.line_picker_trim)
        elif state == 0:
            self.line_value = self.line_picker_trim.value()
            self.plt_species.removeItem(self.line_picker_trim)
            self.sig_line_picked.emit()


