
from PySide6.QtCore import (QSize, Qt)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QPushButton, QVBoxLayout)
from PySide6.QtCore import (Slot, Signal)
import pyqtgraph
import data_models as dms
import numpy as np
import copy


class PlotWidget(QFrame):

    sig_data_updated = Signal()
    sig_line_region_picked = Signal()
    sig_set_enable = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(1)

        self.data_model = dms.DataModel()
        self.region_values = None
        self.line_value = None

        plt_win = pyqtgraph.GraphicsLayoutWidget()
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

        pen = pyqtgraph.mkPen(color='w', width=3)
        self.region_picker_import = pyqtgraph.LinearRegionItem(pen=pen)
        self.line_picker_trim = pyqtgraph.InfiniteLine(pen=pen, movable=True)
        pen.setStyle(Qt.DotLine)
        self.region_picker_trim = pyqtgraph.LinearRegionItem(pen=pen)
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
        self.plt_error.sigRangeChanged.connect(self.slt_error_view_range)

    @Slot(object)
    def slt_update_trim(self):
        [min_val, max_val] = self.region_picker_import.getRegion()
        x_raw = self.data_model.data.x_raw
        ind = np.logical_and(x_raw >= min_val, x_raw <= max_val)
        x_temp = x_raw[ind]
        y_temp = self.data_model.data.y_raw[ind]
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

    @Slot(object, object)
    def slt_error_view_range(self, arg1, arg2):
        text_item = None
        for item in self.plt_error.items:
            if isinstance(item, pyqtgraph.TextItem):
                text_item = item
                break
        if text_item is None:
            return
        xr, yr = arg2
        dx = xr[1] - xr[0]
        dy = yr[1] - yr[0]
        pad = 0.1
        px = xr[1] - dx * pad
        py = yr[1] - dy * pad
        text_item.setPos(px, py)
        text_item.updateTextPos()

    def _pick_region_import(self, state: int):
        if state == 1:  # connect picker
            min_x = np.min(self.data_model.data.x_trim)
            max_x = np.max(self.data_model.data.x_trim)
            self.region_picker_import.setRegion([min_x, max_x])
            self.plt_import.addItem(self.region_picker_import)
            self.sig_set_enable.emit(False)
        elif state == -1:  # cancel and close piker
            self.plt_import.removeItem(self.region_picker_import)
            self.curve_trim.setData(self.data_model.data.x_trim, self.data_model.data.y_trim)
            self.curve_raw.setData(self.data_model.data.x_trim, self.data_model.data.y_trim)
            self.sig_set_enable.emit(True)
        elif state == 0:  # accept and close picker
            data = self.curve_trim.getData()
            self.data_model.data.x_trim = data[0]
            self.data_model.data.y_trim = data[1]
            self.plt_import.removeItem(self.region_picker_import)
            self.sig_data_updated.emit()
            self.sig_set_enable.emit(True)

    def pick_line_region_trim(self, state: int, line: float, x1: float, x2: float):
        if state == 1:  # connect picker
            if x1 == -1 and x2 == -1 and line == -1:
                vr = self.plt_species.viewRange()[0]
                x1, x2 = vr[0], vr[1]
                dx = (x2 - x1) * 0.05
                x1 += dx
                x2 -= dx
                line = 0.5 * (x1 + x2)
            self.region_picker_trim.setRegion([x1, x2])
            self.line_picker_trim.setValue(line)
            self.plt_species.addItem(self.region_picker_trim)
            self.plt_species.addItem(self.line_picker_trim)
        elif state == 0:  # accept and close picker
            self.region_values = self.region_picker_trim.getRegion()
            self.line_value = self.line_picker_trim.value()
            self.plt_species.removeItem(self.region_picker_trim)
            self.plt_species.removeItem(self.line_picker_trim)
            self.sig_line_region_picked.emit()

    def _plot_species(self, index=None):
        for i in range(len(self.data_model.model)):
            xx, yy = self.data_model.model[i].get_xy()
            if xx is not None and yy is not None:
                curve = self.plt_species.plot(pen=pyqtgraph.mkPen(color='magenta', width=2))
                curve.setData(xx, yy)
        if index is not None:
            xx, yy = self.data_model.model[index].get_xy()
            if xx is not None and yy is not None:
                brush = pyqtgraph.mkBrush(color='magenta')
                # brush.setStyle(Qt.BrushStyle.BDiagPattern)
                brush.setStyle(Qt.BrushStyle.DiagCrossPattern)
                pen = pyqtgraph.mkPen(color='magenta', width=2)
                curve = self.plt_species.plot(pen=pen, fillLevel=0)
                curve.setBrush(brush)
                curve.setData(xx, yy)
            else:
                if self.data_model.model[index].type == dms.Types.EXP:
                    return
                x_1 = self.data_model.model[index].gauss.center.min
                x_2 = self.data_model.model[index].gauss.center.value
                x_3 = self.data_model.model[index].gauss.center.max
                pen = pyqtgraph.mkPen(color='cyan', width=1, style=Qt.DotLine)
                curve_1 = pyqtgraph.InfiniteLine(pen=pen, movable=False)
                self.plt_species.addItem(curve_1)
                curve_1.setValue(x_1)
                pen.setStyle(Qt.SolidLine)
                curve_2 = pyqtgraph.InfiniteLine(pen=pen, movable=False)
                self.plt_species.addItem(curve_2)
                curve_2.setValue(x_2)
                pen.setStyle(Qt.DotLine)
                curve_3 = pyqtgraph.InfiniteLine(pen=pen, movable=False)
                self.plt_species.addItem(curve_3)
                curve_3.setValue(x_3)

    def plot_data(self, data_model: dms.DataModel, index=None):
        self.data_model = copy.deepcopy(data_model)
        self.plt_import.clear()
        self.plt_species.clear()
        self.plt_model.clear()
        self.plt_error.clear()
        self.plt_import.addItem(self.curve_import)
        self.plt_species.addItem(self.curve_trim)
        self.plt_model.addItem(self.curve_raw)
        self.curve_import.setData(self.data_model.data.x_raw, self.data_model.data.y_raw)
        self.curve_trim.setData(self.data_model.data.x_trim, self.data_model.data.y_trim)
        self.curve_raw.setData(self.data_model.data.x_trim, self.data_model.data.y_trim)
        if self.data_model.data.y_model is not None:
            curve_m = self.plt_model.plot(pen=pyqtgraph.mkPen(color='magenta', width=2))
            curve_r = self.plt_error.plot(pen='g')
            curve_m.setData(self.data_model.data.x_trim, self.data_model.data.y_model)
            curve_r.setData(self.data_model.data.x_trim, self.data_model.data.residual)
            rmsd = np.sqrt(np.mean(self.data_model.data.residual ** 2))
            px = np.max(self.data_model.data.x_trim)
            py = np.max(self.data_model.data.residual)
            text_item = pyqtgraph.TextItem(f"RMSD = {rmsd: .6f}", pyqtgraph.mkColor("white"), anchor=(1, 0))
            self.plt_error.addItem(text_item)
            text_item.setPos(px, py)
        self._plot_species(index)

    def get_data(self):
        return copy.deepcopy(self.data_model.data)

    def get_region_values(self):
        return self.region_values

    def get_line_value(self):
        return self.line_value
