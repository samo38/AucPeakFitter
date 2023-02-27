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
    QMainWindow, QSizePolicy, QStatusBar, QWidget)

from embed_widgets import (ImportWidget, SpeciesControl, SpeciesList)
from plot_widget import PlotWidget
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(779, 551)
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
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.graphicsView = PlotWidget(self.frm_plot)
        self.graphicsView.setObjectName(u"graphicsView")

        self.horizontalLayout.addWidget(self.graphicsView)


        self.gridLayout.addWidget(self.frm_plot, 1, 1, 1, 1)

        self.frm_ctrl = SpeciesControl(self.centralwidget)
        self.frm_ctrl.setObjectName(u"frm_ctrl")
        self.frm_ctrl.setFrameShape(QFrame.NoFrame)
        self.frm_ctrl.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frm_ctrl, 2, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.st_bar = QStatusBar(MainWindow)
        self.st_bar.setObjectName(u"st_bar")
        MainWindow.setStatusBar(self.st_bar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"AUC Peak Decomposition Program", None))
    # retranslateUi

