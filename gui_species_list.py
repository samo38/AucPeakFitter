# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_species_list.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)
import resources_rc

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(200, 431)
        Frame.setMinimumSize(QSize(200, 0))
        Frame.setMaximumSize(QSize(200, 16777215))
        Frame.setFrameShape(QFrame.NoFrame)
        self.verticalLayout_2 = QVBoxLayout(Frame)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frm_scan = QFrame(Frame)
        self.frm_scan.setObjectName(u"frm_scan")
        self.frm_scan.setFrameShape(QFrame.NoFrame)
        self.frm_scan.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frm_scan)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, 0, 20, 0)
        self.label = QLabel(self.frm_scan)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.spin_box = QSpinBox(self.frm_scan)
        self.spin_box.setObjectName(u"spin_box")

        self.horizontalLayout.addWidget(self.spin_box)


        self.verticalLayout_2.addWidget(self.frm_scan)

        self.frm_list = QFrame(Frame)
        self.frm_list.setObjectName(u"frm_list")
        self.frm_list.setFrameShape(QFrame.NoFrame)
        self.frm_list.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frm_list)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lb_sp = QLabel(self.frm_list)
        self.lb_sp.setObjectName(u"lb_sp")

        self.verticalLayout.addWidget(self.lb_sp, 0, Qt.AlignHCenter)

        self.lw_list = QListWidget(self.frm_list)
        self.lw_list.setObjectName(u"lw_list")

        self.verticalLayout.addWidget(self.lw_list)


        self.verticalLayout_2.addWidget(self.frm_list)

        self.frm_run = QFrame(Frame)
        self.frm_run.setObjectName(u"frm_run")
        self.frm_run.setFrameShape(QFrame.NoFrame)
        self.frm_run.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frm_run)
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pb_ctrl = QPushButton(self.frm_run)
        self.pb_ctrl.setObjectName(u"pb_ctrl")
        self.pb_ctrl.setMinimumSize(QSize(20, 20))
        self.pb_ctrl.setMaximumSize(QSize(20, 20))
        self.pb_ctrl.setStyleSheet(u"background-color: rgb(249, 240, 107);")
        icon = QIcon()
        icon.addFile(u":/Icon/Resources/Icons/tune_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_ctrl.setIcon(icon)
        self.pb_ctrl.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.pb_ctrl)

        self.pb_run = QPushButton(self.frm_run)
        self.pb_run.setObjectName(u"pb_run")
        self.pb_run.setMinimumSize(QSize(75, 30))
        self.pb_run.setMaximumSize(QSize(75, 30))
        self.pb_run.setStyleSheet(u"background-color: rgb(255, 190, 111);")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Resources/Icons/sprint_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_run.setIcon(icon1)
        self.pb_run.setIconSize(QSize(25, 25))

        self.horizontalLayout_2.addWidget(self.pb_run)

        self.pb_rep = QPushButton(self.frm_run)
        self.pb_rep.setObjectName(u"pb_rep")
        self.pb_rep.setMinimumSize(QSize(0, 30))
        self.pb_rep.setMaximumSize(QSize(90, 30))
        self.pb_rep.setStyleSheet(u"background-color: rgb(143, 240, 164);")
        icon2 = QIcon()
        icon2.addFile(u":/Icon/Resources/Icons/text_snippet_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_rep.setIcon(icon2)
        self.pb_rep.setIconSize(QSize(25, 25))

        self.horizontalLayout_2.addWidget(self.pb_rep)


        self.verticalLayout_2.addWidget(self.frm_run)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.label.setText(QCoreApplication.translate("Frame", u"Scan Number:", None))
        self.lb_sp.setText(QCoreApplication.translate("Frame", u"List of Species", None))
        self.pb_ctrl.setText("")
        self.pb_run.setText(QCoreApplication.translate("Frame", u"Run", None))
        self.pb_rep.setText(QCoreApplication.translate("Frame", u"Report", None))
    # retranslateUi

