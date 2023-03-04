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
import gui_species_control
import data_models as dms
import copy


class SpeciesControl(QFrame, gui_species_control.Ui_Frame):

    sig_delete = Signal()
    sig_update = Signal()
    sig_add = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.icon_vis = QIcon()
        self.icon_vis.addFile(u":/Icon/Resources/Icons/visibility_FILL0_wght400_GRAD0_opsz48.svg",
                              QSize(), QIcon.Normal, QIcon.Off)
        self.icon_invis = QIcon()
        self.icon_invis.addFile(u":/Icon/Resources/Icons/visibility_off_FILL0_wght400_GRAD0_opsz48.svg",
                                QSize(), QIcon.Normal, QIcon.Off)
        self.state_new = True
        self.sp_name = None
        self.cmb_type.clear()
        self.cmb_type.addItem("Gaussian")
        self.cmb_type.addItem("Exponential")

        self.func = dms.Function(dms.Types.EMPTY)
        self.func_0 = dms.Function(dms.Types.EMPTY)

        self.vis_state = True
        self.cmb_type.currentTextChanged.connect(self.slt_change_function)
        self.pb_deflt.clicked.connect(self.slt_default)
        self.pb_vis.clicked.connect(self.slt_update_vis)
        self.pb_new.clicked.connect(self.slt_export)
        self.cmb_type.setCurrentIndex(0)
        self.slt_change_function('Gaussian')

    @Slot(str)
    def slt_change_function(self, text):
        if text == 'Gaussian':
            self.stacked.setCurrentWidget(self.wg_gaus)
            self.func.type = dms.Types.GAUSS
        elif text == 'Exponential':
            self.stacked.setCurrentWidget(self.wg_exp)
            self.func.type = dms.Types.EXP
        self.__fill_widget()
        self.__update_le_name()

    @Slot()
    def slt_default(self):
        self.func = copy.deepcopy(self.func_0)
        self.vis_state = self.func.visible
        self.__update_cmb_type()
        self.__fill_widget()
        self.__update_vis_btn()
        self.__update_le_name()

    @Slot(bool)
    def slt_update_vis(self):
        self.vis_state = not self.vis_state
        self.__update_vis_btn()
        self.func.visible = self.vis_state
        self.__update_le_name()

    @Slot()
    def slt_export(self):
        if self.func.type == dms.Types.GAUSS:
            params = self.wg_gaus.get_params()
            if params is None:
                return
            self.func.gauss = params
        elif self.func.type == dms.Types.EXP:
            params = self.wg_exp.get_params()
            if params is None:
                return
            self.func.exp = params
        else:
            return
        if self.state_new:
            self.sig_add.emit()
        else:
            self.sig_update.emit()

    def __update_le_name(self):
        le_name = ''
        if self.vis_state:
            if self.func.type == dms.Types.GAUSS:
                le_name = self.sp_name
            elif self.func.type == dms.Types.EXP:
                le_name = "buffer"
        else:
            if self.func.type == dms.Types.GAUSS:
                le_name = f"*{self.sp_name}*"
            elif self.func.type == dms.Types.EXP:
                le_name = "***buffer"
        self.le_name.setText(le_name)
        self.func.name = le_name

    def __update_cmb_type(self):
        if self.func.type == dms.Types.GAUSS:
            self.cmb_type.setCurrentText(u"Gaussian")
        elif self.func.type == dms.Types.EXP:
            self.cmb_type.setCurrentText(u"Exponential")

    def __update_vis_btn(self):
        if self.vis_state:
            self.pb_vis.setText("ON")
            self.pb_vis.setIcon(self.icon_vis)
            self.pb_vis.setStyleSheet("background-color: ;")
        else:
            self.pb_vis.setText("OFF")
            self.pb_vis.setIcon(self.icon_invis)
            self.pb_vis.setStyleSheet("background-color: rgb(220,220,220);")

    def __fill_widget(self):
        if self.func.type == dms.Types.GAUSS:
            self.wg_gaus.fill_widget(self.func.gauss)
        elif self.func.type == dms.Types.EXP:
            self.wg_exp.fill_widget(self.func.exp)

    def __set_left_panel(self, new: bool):
        if new:
            self.pb_del.setEnabled(False)
            self.pb_new.setText("Add")
            self.pb_new.setStyleSheet("background-color: rgb(143, 240, 164);")
            self.state_new = True
        else:
            self.pb_del.setEnabled(False)
            self.pb_del.setStyleSheet("background-color: rgb(246, 97, 81);")
            self.pb_new.setText("Update")
            self.pb_new.setStyleSheet("background-color: rgb(249, 240, 107);")
            self.state_new = False

    def setup(self, x_arr: np.array, index: int, func=None):
        self.wg_gaus.set_min_mid_max(x_arr)
        if func is None:
            self.func = dms.Function(dms.Types.GAUSS)
            self.func_0 = dms.Function(dms.Types.GAUSS)
            self.__set_left_panel(new=True)
            self.sp_name = f"{index}-species"
            self.le_name.setText(self.sp_name)
        else:
            self.func = copy.deepcopy(func)
            self.func_0 = copy.deepcopy(func)
            self.__set_left_panel(new=False)
            self.le_name.setText(self.func.name)
        self.vis_state = self.func.visible
        self.__update_vis_btn()
        self.__update_cmb_type()
        self.__fill_widget()

    def get_func(self):
        return self.func

