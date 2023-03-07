import copy

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

        self.data = dms.Data()
        self.region_values = None
        self.line_value = None
        self.x_1 = None
        self.x_2 = None
        self.x_3 = None

        plt_win = pyqtgraph.GraphicsLayoutWidget()
        # self.plt_species = plt_win.addPlot(title="Trimmed & Decomposed")  # PlotItem
        # self.plt_import = plt_win.addPlot(title="Imported")
        # plt_win.nextRow()
        # self.plt_error = plt_win.addPlot(title="Residuals")
        # self.plt_model = plt_win.addPlot(title="Trimmed & Modeled")

        self.plt_species = plt_win.addPlot(title="Raw & Decomposed Data")  # PlotItem
        self.plt_model = plt_win.addPlot(title="Raw & Modeled Data")
        plt_win.nextRow()
        self.plt_error = plt_win.addPlot(title="Residuals")
        self.plt_import = plt_win.addPlot(title="Imported Data")

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
        lyt_pb.addStretch(1)
        lyt_pb.addWidget(self.pb_region)
        lyt_pb.addWidget(self.pb_set_region)

        pen = pyqtgraph.mkPen(color='y', width=2)
        self.curve_import = self.plt_import.plot(pen=pen)  # PlotDataItem
        self.curve_trim = self.plt_species.plot(pen=pen)
        self.curve_raw = self.plt_model.plot(pen=pen)

        pen = pyqtgraph.mkPen(color='w', width=2)
        self.region_picker_import = pyqtgraph.LinearRegionItem(pen=pen)
        self.region_picker_trim = pyqtgraph.LinearRegionItem(pen=pen)
        self.line_picker_trim = pyqtgraph.InfiniteLine(pen=pen, movable=True)
        # self.picker_raw.setZValue(-10)

        layout = QHBoxLayout()
        layout.setSpacing(1)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.addWidget(plt_win)
        layout.addLayout(lyt_pb)
        self.setLayout(layout)

        self.region_picker_import.sigRegionChanged.connect(self.slt_update_trim)
        self.pb_region.clicked.connect(self.slt_update_region)
        self.pb_set_region.clicked.connect(self.slt_set_region)

    @Slot(object)
    def slt_update_trim(self):
        [min_val, max_val] = self.region_picker_import.getRegion()
        x_raw = self.data.x_raw
        ind = np.logical_and(x_raw >= min_val, x_raw <= max_val)
        x_temp = x_raw[ind]
        y_temp = self.data.y_raw[ind]
        self.curve_trim.setData(x_temp, y_temp)
        self.curve_raw.setData(x_temp, y_temp)

    @Slot(bool)
    def slt_update_region(self, checked):
        # self.pb_reg.setIconSize(QSize(16, 16))
        if checked:
            self.pb_region.setText("Cancel")
            self.pb_region.setIcon(self.icon_cancel)
            self.pb_region.setStyleSheet(u"background-color: rgb(246, 97, 81);")
            self.pb_set_region.setStyleSheet(u"background-color: rgb(143, 240, 164);")
            self.pb_set_region.setEnabled(True)
            self._pick_region_import(1)
        else:
            self.pb_region.setText("Region")
            self.pb_region.setIcon(self.icon_region)
            self.pb_region.setStyleSheet(u"background-color: rgb(249, 240, 107);")
            self.pb_set_region.setStyleSheet(u"")
            self.pb_set_region.setEnabled(False)
            self._pick_region_import(-1)

    @Slot()
    def slt_set_region(self):
        self.pb_region.setText("Region")
        self.pb_region.setChecked(False)
        self.pb_region.setIcon(self.icon_region)
        self.pb_region.setStyleSheet(u"background-color: rgb(249, 240, 107);")
        self.pb_set_region.setStyleSheet(u"")
        self.pb_set_region.setEnabled(False)
        self._pick_region_import(0)

    def _pick_region_import(self, state: int):
        if state == 1:  # connect picker
            min_x = np.min(self.data.x_trim)
            max_x = np.max(self.data.x_trim)
            self.region_picker_import.setRegion([min_x, max_x])
            self.plt_import.addItem(self.region_picker_import)
        elif state == -1:  # cancel and close piker
            self.plt_import.removeItem(self.region_picker_import)
            self.curve_trim.setData(self.data.x_trim, self.data.y_trim)
            self.curve_raw.setData(self.data.x_trim, self.data.y_trim)
        elif state == 0:  # accept and close picker
            data = self.curve_trim.getData()
            self.data.x_trim = data[0]
            self.data.y_trim = data[1]
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

    def _plot_species(self, index=None):
        plot_region = True
        if self.data.y_model is not None and index is not None:
            if self.data.y_model[index] is not None:
                brush = pyqtgraph.mkBrush(color='magenta')
                # brush.setStyle(Qt.BrushStyle.BDiagPattern)
                brush.setStyle(Qt.BrushStyle.DiagCrossPattern)
                pen = pyqtgraph.mkPen(color='magenta', width=2)
                curve = self.plt_species.plot(pen=pen, fillLevel=0)
                curve.setBrush(brush)
                curve.setData(self.data.x_model, self.data.y_model[index])
                plot_region = False
            for i in range(len(self.data.y_model) - 1):
                if self.data.y_model[i] is not None:
                    curve = self.plt_species.plot(pen=pyqtgraph.mkPen(color='magenta', width=2))
                    curve.setData(self.data.x_model, self.data.y_model[i])
        if (self.x_1 is None) or (self.x_2 is None) or (self.x_3 is None):
            plot_region = False
        if plot_region:
            pen = pyqtgraph.mkPen(color='cyan', width=1, style=Qt.DotLine)
            curve_1 = pyqtgraph.InfiniteLine(pen=pen, movable=False)
            self.plt_species.addItem(curve_1)
            curve_1.setValue(self.x_1)
            pen.setStyle(Qt.SolidLine)
            curve_2 = pyqtgraph.InfiniteLine(pen=pen, movable=False)
            self.plt_species.addItem(curve_2)
            curve_2.setValue(self.x_2)
            pen.setStyle(Qt.DotLine)
            curve_3 = pyqtgraph.InfiniteLine(pen=pen, movable=False)
            self.plt_species.addItem(curve_3)
            curve_3.setValue(self.x_3)

    def plot_data(self, data: dms.Data, index=None, x1=None, x2=None, x3=None):
        self.data = copy.deepcopy(data)
        self.plt_import.clear()
        self.plt_species.clear()
        self.plt_model.clear()
        self.plt_error.clear()
        self.plt_import.addItem(self.curve_import)
        self.plt_species.addItem(self.curve_trim)
        self.plt_model.addItem(self.curve_raw)
        self.x_1 = x1
        self.x_2 = x2
        self.x_3 = x3
        self.curve_import.setData(self.data.x_raw, self.data.y_raw)
        self.curve_trim.setData(self.data.x_trim, self.data.y_trim)
        self.curve_raw.setData(self.data.x_trim, self.data.y_trim)
        if self.data.y_model is not None:
            curve_m = self.plt_model.plot(pen=pyqtgraph.mkPen(color='magenta', width=2))
            curve_r = self.plt_error.plot(pen='g')
            curve_m.setData(self.data.x_model, self.data.y_model[-1])
            curve_r.setData(self.data.x_trim, self.data.residual)
            rmsd = np.sqrt(np.mean(self.data.residual ** 2))
            x_min = np.min(self.data.x_trim)
            x_max = np.max(self.data.x_trim)
            px = x_min + 0.5 * (x_max - x_min)
            py = np.max(self.data.residual)
            rmsd_item = pyqtgraph.TextItem(f"RMSD = {rmsd: .6f}", pyqtgraph.mkColor("white"), anchor=(0.5, 0))
            self.plt_error.addItem(rmsd_item)
            rmsd_item.setPos(px, py)

        self._plot_species(index)

    def get_data(self):
        self.data.clear_modeled()
        return copy.deepcopy(self.data)

    def get_region_values(self):
        return self.region_values

    def get_line_value(self):
        return self.line_value
