# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

from embed_widgets import (ImportWidget, SpeciesControl, SpeciesList)
from plot_widget import PlotWidget
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(779, 551)
        icon = QIcon()
        icon.addFile(u":/Icon/Resources/Icons/App_t.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"@font-face {\n"
"    font-family: Heebo;\n"
"    src: url(:/Font/Resources/Font/Heebo-VariableFont_wght.ttf) format(\"truetype\");\n"
"}\n"
"*{\n"
"color: #000000;\n"
"font-family: Heebo;\n"
"font-size: 12px;\n"
"font-weight: bold;\n"
"background: none;\n"
"}\n"
"#centralwidget{\n"
"background-color: rgb(245,245,245);\n"
"}\n"
"\n"
"")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.frm_open = ImportWidget(self.centralwidget)
        self.frm_open.setObjectName(u"frm_open")
        self.frm_open.setFrameShape(QFrame.StyledPanel)
        self.frm_open.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frm_open, 0, 0, 1, 2)

        self.frm_list = SpeciesList(self.centralwidget)
        self.frm_list.setObjectName(u"frm_list")
        self.frm_list.setFrameShape(QFrame.StyledPanel)
        self.frm_list.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frm_list, 1, 0, 1, 1)

        self.frm_plot = QFrame(self.centralwidget)
        self.frm_plot.setObjectName(u"frm_plot")
        self.frm_plot.setFrameShape(QFrame.StyledPanel)
        self.frm_plot.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frm_plot)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.wg_plot = PlotWidget(self.frm_plot)
        self.wg_plot.setObjectName(u"wg_plot")

        self.horizontalLayout.addWidget(self.wg_plot)

        self.frame = QFrame(self.frm_plot)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pb_reg = QPushButton(self.frame)
        self.pb_reg.setObjectName(u"pb_reg")
        self.pb_reg.setMinimumSize(QSize(75, 0))
        self.pb_reg.setMaximumSize(QSize(75, 16777215))
        self.pb_reg.setStyleSheet(u"background-color: rgb(249, 240, 107);")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Resources/Icons/horizontal_distribute_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_reg.setIcon(icon1)
        self.pb_reg.setIconSize(QSize(16, 16))
        self.pb_reg.setCheckable(True)
        self.pb_reg.setAutoDefault(False)
        self.pb_reg.setFlat(False)

        self.verticalLayout.addWidget(self.pb_reg)

        self.pb_set_reg = QPushButton(self.frame)
        self.pb_set_reg.setObjectName(u"pb_set_reg")
        self.pb_set_reg.setMinimumSize(QSize(75, 0))
        self.pb_set_reg.setMaximumSize(QSize(75, 16777215))
        self.pb_set_reg.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/Icon/Resources/Icons/check_circle_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_set_reg.setIcon(icon2)
        self.pb_set_reg.setIconSize(QSize(16, 16))

        self.verticalLayout.addWidget(self.pb_set_reg, 0, Qt.AlignTop)


        self.horizontalLayout.addWidget(self.frame)


        self.gridLayout.addWidget(self.frm_plot, 1, 1, 1, 1)

        self.frm_ctrl = SpeciesControl(self.centralwidget)
        self.frm_ctrl.setObjectName(u"frm_ctrl")
        self.frm_ctrl.setFrameShape(QFrame.NoFrame)
        self.frm_ctrl.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frm_ctrl, 2, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.pb_reg.setDefault(False)
        self.pb_set_reg.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"AUC Peak Decomposition Program", None))
        self.pb_reg.setText(QCoreApplication.translate("MainWindow", u"Region", None))
        self.pb_set_reg.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
    # retranslateUi

