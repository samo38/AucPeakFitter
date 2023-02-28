from PySide6 import QtWidgets
from PySide6.QtCore import Slot, Signal
import pyqtgraph as pg
import numpy as np
import data_models as dm


class PlotWidget(pg.GraphicsLayoutWidget):

    sig_data_models_updated = Signal(dm.DataModels)

    def __init__(self, parent=None):
        super().__init__(parent=parent, show=True)

        self.data_models = dm.DataModels()
        self.x_raw = None
        self.y_raw = None
        self.x_trim = None
        self.y_trim = None

        self.resize(500, 500)
        self.plot_lu = self.addPlot(title="Trimmed & Decomposed")  # PlotItem
        self.plot_ru = self.addPlot(title="Imported")
        self.nextRow()
        self.plot_ld = self.addPlot(title="Residuals")
        self.plot_rd = self.addPlot(title="Trimmed & Modeled")

        self.curve_raw = self.plot_ru.plot(pen='y')  # PlotDataItem
        self.curve_trim = self.plot_lu.plot(pen='y')

        self.picker_reg_raw = pg.LinearRegionItem(pen=pg.mkPen("white"))
        self.picker_reg_trim = pg.LinearRegionItem()
        self.picker_reg_trim_val = None
        self.picker_line_trim = pg.InfiniteLine(pen="white", movable=True)
        self.picker_line_trim_val = None
        # self.picker_raw.setZValue(-10)

        self.picker_reg_raw.sigRegionChanged.connect(self.update_trim)

    @Slot()
    def update_trim(self):
        [min_val, max_val] = self.picker_reg_raw.getRegion()
        ind = np.logical_and(self.x_raw >= min_val, self.x_raw <= max_val)
        x_temp = self.x_raw[ind]
        y_temp = self.y_raw[ind]
        self.plot_trim(x_temp, y_temp)

    def import_model(self, data_models: dm.DataModels):
        self.data_models = data_models
        self.x_raw = data_models.x_raw
        self.y_raw = data_models.y_raw
        self.x_trim = data_models.x_trim
        self.y_trim = data_models.y_trim
        self.plot_raw()
        self.plot_trim()

    def plot_raw(self):
        self.curve_raw.setData(self.x_raw, self.y_raw)

    def plot_trim(self, x=None, y=None):
        if (x is not None) and (y is not None):
            self.curve_trim.setData(x, y)
        else:
            self.curve_trim.setData(self.x_trim, self.y_trim)

    def pick_region_raw(self, state: int):
        if state == 1:  # connect picker
            self.picker_reg_raw.setRegion([np.min(self.x_trim), np.max(self.x_trim)])
            self.plot_ru.addItem(self.picker_reg_raw)
        elif state == -1:  # cancel and close piker
            self.plot_ru.removeItem(self.picker_reg_raw)
            self.plot_trim()
        elif state == 0:  # accept and close picker
            data = self.curve_trim.getData()
            self.x_trim = data[0]
            self.y_trim = data[1]
            self.data_models.x_trim = self.x_trim
            self.data_models.y_trim = self.y_trim
            self.plot_ru.removeItem(self.picker_reg_raw)
            self.sig_data_models_updated.emit(self.data_models)

    def pick_line_trim(self, state: int, val: float):
        if state == 1:
            self.picker_line_trim.setValue(val)
            self.plot_lu.addItem(self.picker_line_trim)
        elif state == 0:
            self.picker_line_trim_val = self.picker_line_trim.value()
            self.plot_lu.removeItem(self.picker_line_trim)
