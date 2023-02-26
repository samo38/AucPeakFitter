# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_species_control.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QStackedWidget, QWidget)

from embed_models import (ExponentialControl, GaussianControl)
import resources_rc

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(681, 140)
        Frame.setMinimumSize(QSize(0, 140))
        Frame.setMaximumSize(QSize(16777215, 140))
        self.horizontalLayout = QHBoxLayout(Frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.group = QGroupBox(Frame)
        self.group.setObjectName(u"group")
        self.group.setMinimumSize(QSize(0, 0))
        self.group.setMaximumSize(QSize(16777215, 16777215))
        self.group.setStyleSheet(u"#le_name{\n"
"font-weight: normal;\n"
"}\n"
"")
        self.horizontalLayout_2 = QHBoxLayout(self.group)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frm_new = QFrame(self.group)
        self.frm_new.setObjectName(u"frm_new")
        self.frm_new.setMinimumSize(QSize(170, 0))
        self.frm_new.setMaximumSize(QSize(170, 10000))
        self.frm_new.setFrameShape(QFrame.NoFrame)
        self.frm_new.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frm_new)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pb_new = QPushButton(self.frm_new)
        self.pb_new.setObjectName(u"pb_new")
        self.pb_new.setMinimumSize(QSize(70, 25))
        self.pb_new.setMaximumSize(QSize(70, 25))
        self.pb_new.setStyleSheet(u"background-color: rgb(249, 240, 107);")
        icon = QIcon()
        icon.addFile(u":/Icon/Resources/Icons/add_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_new.setIcon(icon)
        self.pb_new.setIconSize(QSize(20, 20))

        self.gridLayout.addWidget(self.pb_new, 0, 0, 1, 1)

        self.pb_del = QPushButton(self.frm_new)
        self.pb_del.setObjectName(u"pb_del")
        self.pb_del.setMinimumSize(QSize(90, 25))
        self.pb_del.setMaximumSize(QSize(90, 25))
        self.pb_del.setStyleSheet(u"background-color: rgb(224, 27, 36);")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Resources/Icons/delete_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_del.setIcon(icon1)
        self.pb_del.setIconSize(QSize(20, 20))

        self.gridLayout.addWidget(self.pb_del, 0, 1, 1, 1)

        self.pb_vis = QPushButton(self.frm_new)
        self.pb_vis.setObjectName(u"pb_vis")
        self.pb_vis.setMinimumSize(QSize(70, 25))
        self.pb_vis.setMaximumSize(QSize(70, 25))
        self.pb_vis.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/Icon/Resources/Icons/visibility_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_vis.setIcon(icon2)
        self.pb_vis.setIconSize(QSize(20, 20))

        self.gridLayout.addWidget(self.pb_vis, 1, 0, 1, 1)

        self.lb_warn = QLabel(self.frm_new)
        self.lb_warn.setObjectName(u"lb_warn")
        self.lb_warn.setMinimumSize(QSize(90, 25))
        self.lb_warn.setMaximumSize(QSize(90, 25))
        self.lb_warn.setStyleSheet(u"color: rgb(224, 27, 36);")
        self.lb_warn.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lb_warn, 1, 1, 1, 1)

        self.lb_name = QLabel(self.frm_new)
        self.lb_name.setObjectName(u"lb_name")
        self.lb_name.setMinimumSize(QSize(70, 25))
        self.lb_name.setMaximumSize(QSize(70, 25))
        self.lb_name.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lb_name, 2, 0, 1, 1)

        self.le_name = QLineEdit(self.frm_new)
        self.le_name.setObjectName(u"le_name")
        self.le_name.setMinimumSize(QSize(90, 25))
        self.le_name.setMaximumSize(QSize(90, 25))

        self.gridLayout.addWidget(self.le_name, 2, 1, 1, 1)

        self.lb_type = QLabel(self.frm_new)
        self.lb_type.setObjectName(u"lb_type")
        self.lb_type.setMinimumSize(QSize(70, 25))
        self.lb_type.setMaximumSize(QSize(70, 25))
        self.lb_type.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.lb_type, 3, 0, 1, 1)

        self.cmb_type = QComboBox(self.frm_new)
        self.cmb_type.setObjectName(u"cmb_type")
        self.cmb_type.setMinimumSize(QSize(90, 25))
        self.cmb_type.setMaximumSize(QSize(90, 25))

        self.gridLayout.addWidget(self.cmb_type, 3, 1, 1, 1)


        self.horizontalLayout_2.addWidget(self.frm_new, 0, Qt.AlignLeft)

        self.stacked = QStackedWidget(self.group)
        self.stacked.setObjectName(u"stacked")
        self.wg_gaus = GaussianControl()
        self.wg_gaus.setObjectName(u"wg_gaus")
        self.stacked.addWidget(self.wg_gaus)
        self.wg_exp = ExponentialControl()
        self.wg_exp.setObjectName(u"wg_exp")
        self.stacked.addWidget(self.wg_exp)

        self.horizontalLayout_2.addWidget(self.stacked)


        self.horizontalLayout.addWidget(self.group)


        self.retranslateUi(Frame)

        self.stacked.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.group.setTitle(QCoreApplication.translate("Frame", u"Species Control", None))
        self.pb_new.setText(QCoreApplication.translate("Frame", u"New", None))
        self.pb_del.setText(QCoreApplication.translate("Frame", u"Delete", None))
        self.pb_vis.setText(QCoreApplication.translate("Frame", u"ON", None))
        self.lb_warn.setText(QCoreApplication.translate("Frame", u"Not Ready", None))
        self.lb_name.setText(QCoreApplication.translate("Frame", u"Name:", None))
        self.lb_type.setText(QCoreApplication.translate("Frame", u"Type:", None))
    # retranslateUi

