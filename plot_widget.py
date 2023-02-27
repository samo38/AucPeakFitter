from PySide6 import QtWidgets
from PySide6.QtCore import Slot, Signal
import pyqtgraph as pg
import numpy as np


class DataRegion:

    def __init__(self, min_val=None, max_val=None, state=None):
        self.min_val = min_val
        self.max_val = max_val
        self.state = state

    def getter(self):
        return np.array([self.min_val, self.max_val, self.state])

    def setter(self, min_val, max_val, state):
        self.min_val = min_val
        self.max_val = max_val
        self.state = state


# class PlotWidget(QtWidgets.QGraphicsView):
#
#     def __init__(self, parent=None):
#         super().__init__(parent=parent)
#         self.picker = None
#
#         self.graph_lyt_wg = pg.GraphicsLayoutWidget(show=True)
#         # pg.setConfigOptions(antialias=True)
#         self.graph_lyt_wg.resize(600, 400)
#
#         self.plot_lu = self.graph_lyt_wg.addPlot(title="Deconvoluted Graphs")
#         self.plot_ru = self.graph_lyt_wg.addPlot(title="Imported Data")
#         self.graph_lyt_wg.nextRow()
#         self.plot_ld = self.graph_lyt_wg.addPlot(title="Residuals")
#         self.plot_rd = self.graph_lyt_wg.addPlot(title="Raw & Modeled Graphs")
#
#         self.raw_curve = self.plot_ru.plot(pen='y')
#         self.raw_minmax = DataRegion()
#
#         self.raw_curve_sel = self.plot_lu.plot(pen='y')
#
#
#         # self.p1.plot(self.x, self.y, pen=(255, 255, 255, 200))
#         # self.picker_reg = pg.LinearRegionItem([self.min_val, self.max_val])
#         # self.picker_reg.setZValue(-10)
#         # self.p1.addItem(self.picker_reg)
#         #
#         # self.p2 = self.plot_win.addPlot(title="Zoom on selected region")
#         # self.p2.plot(self.x, self.y)
#         # self.picker_reg.sigRegionChanged.connect(self.update_plot)
#         # # self.p2.sigXRangeChanged.connect(self.update_region)
#         # self.update_plot()
#         #
#         # layout = QtWidgets.QHBoxLayout()
#         # self.setLayout(layout)
#         #
#         # layout_pick = QtWidgets.QVBoxLayout()
#         # layout_pick.addWidget(self.pb_pick_reg)
#         # layout_pick.addWidget(self.pb_pick_lin)
#         # layout.addLayout(layout_pick)
#         # layout.addWidget(self.plot_win)
#
#     # @Slot()
#     # def update_plot(self):
#     #     reg = self.picker_reg.getRegion()
#     #     self.min_val = reg[0]
#     #     self.max_val = reg[1]
#     #     ind = np.logical_and(self.x >= reg[0], self.x <= reg[1])
#     #     self.x_cut = self.x[ind]
#     #     self.y_cut = self.y[ind]
#     #     self.p2.plot(self.x_cut, self.y_cut)
#         # self.p2.setXRange(*self.picker_reg.getRegion(), padding=0)
#
#     # @Slot()
#     # def update_region(self):
#     #     self.picker_reg.setRegion(self.p2.getViewBox().viewRange()[0])
#
#


class PlotWidget(pg.GraphicsLayoutWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent, show=True)

        self.resize(600, 400)

        self.plot_lu = self.addPlot(title="Deconvoluted Graphs")
        self.plot_ru = self.addPlot(title="Imported Data")
        self.nextRow()
        self.plot_ld = self.addPlot(title="Residuals")
        self.plot_rd = self.addPlot(title="Raw & Modeled Graphs")

        self.curve_raw = self.plot_ru.plot(pen='y')
        self.minmax_raw = DataRegion()
        self.curve_trim = self.plot_lu.plot(pen='y')

        self.picker_raw = pg.LinearRegionItem()
        self.picker_raw.setZValue(-10)
        self.plot_ru.addItem(self.picker_raw)

        # self.p1.plot(self.x, self.y, pen=(255, 255, 255, 200))
        # self.picker_reg =
        # self.picker_reg.setZValue(-10)
        # self.p1.addItem(self.picker_reg)
        #
        # self.p2 = self.plot_win.addPlot(title="Zoom on selected region")
        # self.p2.plot(self.x, self.y)
        # self.picker_reg.sigRegionChanged.connect(self.update_plot)
        # # self.p2.sigXRangeChanged.connect(self.update_region)
        # self.update_plot()
        #
        # layout = QtWidgets.QHBoxLayout()
        # self.setLayout(layout)
        #
        # layout_pick = QtWidgets.QVBoxLayout()
        # layout_pick.addWidget(self.pb_pick_reg)
        # layout_pick.addWidget(self.pb_pick_lin)
        # layout.addLayout(layout_pick)
        # layout.addWidget(self.plot_win)

    # @Slot()
    # def update_plot(self):
    #     reg = self.picker_reg.getRegion()
    #     self.min_val = reg[0]
    #     self.max_val = reg[1]
    #     ind = np.logical_and(self.x >= reg[0], self.x <= reg[1])
    #     self.x_cut = self.x[ind]
    #     self.y_cut = self.y[ind]
    #     self.p2.plot(self.x_cut, self.y_cut)
        # self.p2.setXRange(*self.picker_reg.getRegion(), padding=0)

    # @Slot()
    # def update_region(self):
    #     self.picker_reg.setRegion(self.p2.getViewBox().viewRange()[0])


