# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_import.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(774, 80)
        Frame.setMinimumSize(QSize(0, 80))
        Frame.setMaximumSize(QSize(16777215, 88))
        Frame.setStyleSheet(u"#le_desc, #le_cell, #le_chan, #le_rpm, #le_temp, #le_type, #le_wavl{\n"
"font-weight: normal;\n"
"}")
        Frame.setLineWidth(1)
        self.horizontalLayout = QHBoxLayout(Frame)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 0, 2, 0)
        self.frm_logo = QFrame(Frame)
        self.frm_logo.setObjectName(u"frm_logo")
        self.frm_logo.setMinimumSize(QSize(120, 70))
        self.frm_logo.setMaximumSize(QSize(120, 70))
        self.frm_logo.setFrameShape(QFrame.NoFrame)
        self.frm_logo.setFrameShadow(QFrame.Raised)
        self.frm_logo.setLineWidth(1)
        self.verticalLayout = QVBoxLayout(self.frm_logo)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lb_logo = QLabel(self.frm_logo)
        self.lb_logo.setObjectName(u"lb_logo")
        self.lb_logo.setMinimumSize(QSize(60, 38))
        self.lb_logo.setMaximumSize(QSize(60, 38))
        self.lb_logo.setPixmap(QPixmap(u":/Icon/Resources/Icons/WinLogo.png"))
        self.lb_logo.setScaledContents(True)

        self.verticalLayout.addWidget(self.lb_logo, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.lb_text = QLabel(self.frm_logo)
        self.lb_text.setObjectName(u"lb_text")
        self.lb_text.setAlignment(Qt.AlignCenter)
        self.lb_text.setWordWrap(True)

        self.verticalLayout.addWidget(self.lb_text, 0, Qt.AlignHCenter|Qt.AlignBottom)


        self.horizontalLayout.addWidget(self.frm_logo)

        self.frm_open = QFrame(Frame)
        self.frm_open.setObjectName(u"frm_open")
        self.frm_open.setFrameShape(QFrame.NoFrame)
        self.frm_open.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frm_open)
        self.verticalLayout_4.setSpacing(1)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frm_1 = QFrame(self.frm_open)
        self.frm_1.setObjectName(u"frm_1")
        self.frm_1.setMinimumSize(QSize(0, 30))
        self.frm_1.setMaximumSize(QSize(16777215, 30))
        self.frm_1.setFrameShape(QFrame.NoFrame)
        self.frm_1.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frm_1)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pb_open = QPushButton(self.frm_1)
        self.pb_open.setObjectName(u"pb_open")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_open.sizePolicy().hasHeightForWidth())
        self.pb_open.setSizePolicy(sizePolicy)
        self.pb_open.setMinimumSize(QSize(130, 25))
        self.pb_open.setMaximumSize(QSize(130, 25))
        font = QFont()
        font.setFamilies([u"Heebo"])
        font.setBold(False)
        self.pb_open.setFont(font)
        self.pb_open.setStyleSheet(u"background-color: rgb(135, 206, 235);\n"
"")
        icon = QIcon()
        icon.addFile(u":/Icon/Resources/Icons/file_open_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_open.setIcon(icon)
        self.pb_open.setIconSize(QSize(25, 25))

        self.horizontalLayout_4.addWidget(self.pb_open)

        self.lb_desc = QLabel(self.frm_1)
        self.lb_desc.setObjectName(u"lb_desc")
        sizePolicy.setHeightForWidth(self.lb_desc.sizePolicy().hasHeightForWidth())
        self.lb_desc.setSizePolicy(sizePolicy)
        self.lb_desc.setMinimumSize(QSize(93, 0))
        self.lb_desc.setMaximumSize(QSize(93, 16777215))
        font1 = QFont()
        font1.setFamilies([u"all-the-icons"])
        font1.setBold(False)
        self.lb_desc.setFont(font1)

        self.horizontalLayout_4.addWidget(self.lb_desc)

        self.le_desc = QLineEdit(self.frm_1)
        self.le_desc.setObjectName(u"le_desc")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.le_desc.sizePolicy().hasHeightForWidth())
        self.le_desc.setSizePolicy(sizePolicy1)
        self.le_desc.setMinimumSize(QSize(416, 0))
        self.le_desc.setMaximumSize(QSize(416, 16777215))
        self.le_desc.setFont(font)
        self.le_desc.setLayoutDirection(Qt.LeftToRight)
        self.le_desc.setStyleSheet(u"")
        self.le_desc.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.le_desc)

        self.horizontalLayout_4.setStretch(2, 1)

        self.verticalLayout_4.addWidget(self.frm_1, 0, Qt.AlignLeft)

        self.frm_2 = QFrame(self.frm_open)
        self.frm_2.setObjectName(u"frm_2")
        self.frm_2.setMinimumSize(QSize(0, 30))
        self.frm_2.setMaximumSize(QSize(16777215, 30))
        self.frm_2.setFrameShape(QFrame.NoFrame)
        self.frm_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frm_2)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.lb_type = QLabel(self.frm_2)
        self.lb_type.setObjectName(u"lb_type")
        self.lb_type.setMinimumSize(QSize(38, 0))
        self.lb_type.setMaximumSize(QSize(38, 16777215))

        self.horizontalLayout_5.addWidget(self.lb_type)

        self.le_type = QLineEdit(self.frm_2)
        self.le_type.setObjectName(u"le_type")
        self.le_type.setMinimumSize(QSize(30, 0))
        self.le_type.setMaximumSize(QSize(30, 16777215))
        self.le_type.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.le_type)

        self.lb_cell = QLabel(self.frm_2)
        self.lb_cell.setObjectName(u"lb_cell")
        self.lb_cell.setMinimumSize(QSize(36, 0))
        self.lb_cell.setMaximumSize(QSize(36, 16777215))
        self.lb_cell.setFont(font)

        self.horizontalLayout_5.addWidget(self.lb_cell)

        self.le_cell = QLineEdit(self.frm_2)
        self.le_cell.setObjectName(u"le_cell")
        self.le_cell.setMinimumSize(QSize(30, 0))
        self.le_cell.setMaximumSize(QSize(30, 16777215))
        self.le_cell.setFont(font)
        self.le_cell.setStyleSheet(u"")
        self.le_cell.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.le_cell)

        self.lb_chan = QLabel(self.frm_2)
        self.lb_chan.setObjectName(u"lb_chan")
        self.lb_chan.setMinimumSize(QSize(66, 0))
        self.lb_chan.setMaximumSize(QSize(66, 16777215))

        self.horizontalLayout_5.addWidget(self.lb_chan)

        self.le_chan = QLineEdit(self.frm_2)
        self.le_chan.setObjectName(u"le_chan")
        self.le_chan.setMinimumSize(QSize(30, 0))
        self.le_chan.setMaximumSize(QSize(30, 16777215))
        self.le_chan.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.le_chan)

        self.lb_wavl = QLabel(self.frm_2)
        self.lb_wavl.setObjectName(u"lb_wavl")
        self.lb_wavl.setMinimumSize(QSize(91, 0))
        self.lb_wavl.setMaximumSize(QSize(91, 16777215))

        self.horizontalLayout_5.addWidget(self.lb_wavl)

        self.le_wavl = QLineEdit(self.frm_2)
        self.le_wavl.setObjectName(u"le_wavl")
        self.le_wavl.setMinimumSize(QSize(60, 0))
        self.le_wavl.setMaximumSize(QSize(60, 16777215))
        self.le_wavl.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.le_wavl)

        self.lb_rpm = QLabel(self.frm_2)
        self.lb_rpm.setObjectName(u"lb_rpm")
        self.lb_rpm.setMinimumSize(QSize(41, 0))
        self.lb_rpm.setMaximumSize(QSize(41, 16777215))
        self.lb_rpm.setFont(font)

        self.horizontalLayout_5.addWidget(self.lb_rpm)

        self.le_rpm = QLineEdit(self.frm_2)
        self.le_rpm.setObjectName(u"le_rpm")
        self.le_rpm.setMinimumSize(QSize(60, 0))
        self.le_rpm.setMaximumSize(QSize(60, 16777215))
        self.le_rpm.setFont(font)
        self.le_rpm.setStyleSheet(u"")
        self.le_rpm.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.le_rpm)

        self.lb_temp = QLabel(self.frm_2)
        self.lb_temp.setObjectName(u"lb_temp")
        self.lb_temp.setMinimumSize(QSize(97, 0))
        self.lb_temp.setMaximumSize(QSize(97, 16777215))
        self.lb_temp.setFont(font)

        self.horizontalLayout_5.addWidget(self.lb_temp)

        self.le_temp = QLineEdit(self.frm_2)
        self.le_temp.setObjectName(u"le_temp")
        self.le_temp.setMinimumSize(QSize(60, 0))
        self.le_temp.setMaximumSize(QSize(60, 16777215))
        self.le_temp.setFont(font)
        self.le_temp.setStyleSheet(u"")
        self.le_temp.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.le_temp)


        self.verticalLayout_4.addWidget(self.frm_2, 0, Qt.AlignLeft)


        self.horizontalLayout.addWidget(self.frm_open)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.lb_logo.setText("")
        self.lb_text.setText(QCoreApplication.translate("Frame", u"AUC Peak Decomposition", None))
        self.pb_open.setText(QCoreApplication.translate("Frame", u"Open AUC File", None))
        self.lb_desc.setText(QCoreApplication.translate("Frame", u"  Description:", None))
        self.lb_type.setText(QCoreApplication.translate("Frame", u"Type:", None))
        self.lb_cell.setText(QCoreApplication.translate("Frame", u" Cell:", None))
        self.lb_chan.setText(QCoreApplication.translate("Frame", u" Channel:", None))
        self.lb_wavl.setText(QCoreApplication.translate("Frame", u" Wavelength:", None))
        self.lb_rpm.setText(QCoreApplication.translate("Frame", u" RPM:", None))
        self.lb_temp.setText(QCoreApplication.translate("Frame", u" Temperature:", None))
    # retranslateUi

