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

        self.resize(400, 400)
        self.plot_lu = self.addPlot(title="Deconvoluted Graphs")  # PlotItem
        self.plot_ru = self.addPlot(title="Imported Data")
        self.nextRow()
        self.plot_ld = self.addPlot(title="Residuals")
        self.plot_rd = self.addPlot(title="Raw & Modeled Graphs")

        self.curve_raw = self.plot_ru.plot(pen='y')  # PlotDataItem
        self.curve_trim = self.plot_lu.plot(pen='y')

        self.picker_reg = pg.LinearRegionItem()
        self.picker_mm = pg.LinearRegionItem()
        self.picker_cen = pg.InfiniteLine()
        # self.picker_raw.setZValue(-10)

        self.picker_reg.sigRegionChanged.connect(self.update_trim)

    @Slot()
    def update_trim(self):
        [min_val, max_val] = self.picker_reg.getRegion()
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
            self.picker_reg.setRegion([np.min(self.x_trim), np.max(self.x_trim)])
            self.plot_ru.addItem(self.picker_reg)
        elif state == -1:  # cancel and close piker
            self.plot_ru.removeItem(self.picker_reg)
            self.plot_trim()
        elif state == 0:  # accept and close picker
            data = self.curve_trim.getData()
            self.x_trim = data[0]
            self.y_trim = data[1]
            self.data_models.x_trim = self.x_trim
            self.data_models.y_trim = self.y_trim
            self.plot_ru.removeItem(self.picker_reg)
            self.sig_data_models_updated.emit(self.data_models)
