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
    QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)

from functions_widgets import (ExponentialControl, GaussianControl)
import resources_rc

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(693, 144)
        Frame.setMinimumSize(QSize(0, 140))
        Frame.setMaximumSize(QSize(16777215, 144))
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
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.group)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(170, 0))
        self.frame.setMaximumSize(QSize(170, 16777215))
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_1 = QFrame(self.frame)
        self.frame_1.setObjectName(u"frame_1")
        self.frame_1.setMinimumSize(QSize(170, 0))
        self.frame_1.setMaximumSize(QSize(170, 10000))
        self.frame_1.setFrameShape(QFrame.NoFrame)
        self.frame_1.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_1)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pb_deflt = QPushButton(self.frame_1)
        self.pb_deflt.setObjectName(u"pb_deflt")
        self.pb_deflt.setMinimumSize(QSize(80, 0))
        self.pb_deflt.setMaximumSize(QSize(80, 16777215))
        icon = QIcon()
        icon.addFile(u":/Icon/Resources/Icons/keyboard_return_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_deflt.setIcon(icon)

        self.gridLayout.addWidget(self.pb_deflt, 1, 1, 1, 1, Qt.AlignLeft)

        self.pb_del = QPushButton(self.frame_1)
        self.pb_del.setObjectName(u"pb_del")
        self.pb_del.setMinimumSize(QSize(80, 0))
        self.pb_del.setMaximumSize(QSize(80, 16777215))
        self.pb_del.setStyleSheet(u"")
        icon1 = QIcon()
        icon1.addFile(u":/Icon/Resources/Icons/delete_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_del.setIcon(icon1)
        self.pb_del.setIconSize(QSize(16, 16))

        self.gridLayout.addWidget(self.pb_del, 0, 1, 1, 1, Qt.AlignLeft)

        self.pb_new = QPushButton(self.frame_1)
        self.pb_new.setObjectName(u"pb_new")
        self.pb_new.setMinimumSize(QSize(80, 0))
        self.pb_new.setMaximumSize(QSize(82, 16777215))
        self.pb_new.setStyleSheet(u"")
        icon2 = QIcon()
        icon2.addFile(u":/Icon/Resources/Icons/add_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_new.setIcon(icon2)
        self.pb_new.setIconSize(QSize(16, 16))

        self.gridLayout.addWidget(self.pb_new, 0, 0, 1, 1, Qt.AlignRight)

        self.pb_vis = QPushButton(self.frame_1)
        self.pb_vis.setObjectName(u"pb_vis")
        self.pb_vis.setMinimumSize(QSize(80, 0))
        self.pb_vis.setMaximumSize(QSize(80, 16777215))
        self.pb_vis.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u":/Icon/Resources/Icons/visibility_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_vis.setIcon(icon3)
        self.pb_vis.setIconSize(QSize(20, 20))
        self.pb_vis.setFlat(True)

        self.gridLayout.addWidget(self.pb_vis, 1, 0, 1, 1, Qt.AlignRight)


        self.verticalLayout.addWidget(self.frame_1)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_2)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.cmb_type = QComboBox(self.frame_2)
        self.cmb_type.setObjectName(u"cmb_type")

        self.gridLayout_2.addWidget(self.cmb_type, 1, 1, 1, 1)

        self.lb_name = QLabel(self.frame_2)
        self.lb_name.setObjectName(u"lb_name")
        self.lb_name.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lb_name, 0, 0, 1, 1, Qt.AlignRight)

        self.lb_type = QLabel(self.frame_2)
        self.lb_type.setObjectName(u"lb_type")
        self.lb_type.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.lb_type, 1, 0, 1, 1, Qt.AlignRight)

        self.le_name = QLineEdit(self.frame_2)
        self.le_name.setObjectName(u"le_name")
        self.le_name.setReadOnly(True)

        self.gridLayout_2.addWidget(self.le_name, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame_2)


        self.horizontalLayout_2.addWidget(self.frame)

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

        self.stacked.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.group.setTitle(QCoreApplication.translate("Frame", u" Species Control", None))
        self.pb_deflt.setText(QCoreApplication.translate("Frame", u"Default", None))
        self.pb_del.setText(QCoreApplication.translate("Frame", u"Delete", None))
        self.pb_new.setText(QCoreApplication.translate("Frame", u"Add", None))
        self.pb_vis.setText(QCoreApplication.translate("Frame", u"ON", None))
        self.lb_name.setText(QCoreApplication.translate("Frame", u"Name:", None))
        self.lb_type.setText(QCoreApplication.translate("Frame", u"Type:", None))
    # retranslateUi

