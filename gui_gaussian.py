# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_gaussian.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(576, 110)
        Form.setMinimumSize(QSize(0, 110))
        Form.setMaximumSize(QSize(16777215, 110))
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.group = QGroupBox(Form)
        self.group.setObjectName(u"group")
        self.group.setStyleSheet(u"#le_cent_mm, #le_cent_val, #le_height, #le_sigma{\n"
"font-weight: normal;\n"
"}")
        self.gridLayout = QGridLayout(self.group)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.group)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)

        self.pb_cent_val = QPushButton(self.group)
        self.pb_cent_val.setObjectName(u"pb_cent_val")
        self.pb_cent_val.setMinimumSize(QSize(55, 0))
        self.pb_cent_val.setMaximumSize(QSize(55, 16777215))
        self.pb_cent_val.setCheckable(True)

        self.gridLayout.addWidget(self.pb_cent_val, 0, 4, 1, 1)

        self.label_3 = QLabel(self.group)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.le_cent_mm = QLineEdit(self.group)
        self.le_cent_mm.setObjectName(u"le_cent_mm")
        self.le_cent_mm.setMinimumSize(QSize(105, 0))
        self.le_cent_mm.setMaximumSize(QSize(105, 16777215))
        self.le_cent_mm.setReadOnly(True)

        self.gridLayout.addWidget(self.le_cent_mm, 0, 6, 1, 1)

        self.fix_center = QCheckBox(self.group)
        self.fix_center.setObjectName(u"fix_center")

        self.gridLayout.addWidget(self.fix_center, 0, 1, 1, 1)

        self.fix_sigma = QCheckBox(self.group)
        self.fix_sigma.setObjectName(u"fix_sigma")

        self.gridLayout.addWidget(self.fix_sigma, 1, 1, 1, 1)

        self.le_amp = QLineEdit(self.group)
        self.le_amp.setObjectName(u"le_amp")
        self.le_amp.setMinimumSize(QSize(55, 0))
        self.le_amp.setMaximumSize(QSize(55, 16777215))
        self.le_amp.setReadOnly(True)

        self.gridLayout.addWidget(self.le_amp, 2, 3, 1, 1)

        self.label_2 = QLabel(self.group)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_7 = QLabel(self.group)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 0, 5, 1, 1)

        self.fix_amp = QCheckBox(self.group)
        self.fix_amp.setObjectName(u"fix_amp")

        self.gridLayout.addWidget(self.fix_amp, 2, 1, 1, 1)

        self.le_sigma = QLineEdit(self.group)
        self.le_sigma.setObjectName(u"le_sigma")
        self.le_sigma.setMinimumSize(QSize(55, 0))
        self.le_sigma.setMaximumSize(QSize(55, 16777215))
        self.le_sigma.setReadOnly(True)

        self.gridLayout.addWidget(self.le_sigma, 1, 3, 1, 1)

        self.label = QLabel(self.group)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.le_cent_val = QLineEdit(self.group)
        self.le_cent_val.setObjectName(u"le_cent_val")
        self.le_cent_val.setMinimumSize(QSize(55, 0))
        self.le_cent_val.setMaximumSize(QSize(55, 16777215))
        self.le_cent_val.setReadOnly(True)

        self.gridLayout.addWidget(self.le_cent_val, 0, 3, 1, 1)

        self.label_4 = QLabel(self.group)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)

        self.pb_cent_mm = QPushButton(self.group)
        self.pb_cent_mm.setObjectName(u"pb_cent_mm")
        self.pb_cent_mm.setMinimumSize(QSize(55, 0))
        self.pb_cent_mm.setMaximumSize(QSize(55, 16777215))
        self.pb_cent_mm.setCheckable(True)

        self.gridLayout.addWidget(self.pb_cent_mm, 0, 7, 1, 1)

        self.label_5 = QLabel(self.group)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)

        self.bound_sigma = QCheckBox(self.group)
        self.bound_sigma.setObjectName(u"bound_sigma")

        self.gridLayout.addWidget(self.bound_sigma, 1, 4, 1, 2)


        self.horizontalLayout.addWidget(self.group, 0, Qt.AlignLeft)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.group.setTitle(QCoreApplication.translate("Form", u"Gaussian Function", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Value:", None))
        self.pb_cent_val.setText(QCoreApplication.translate("Form", u"Set", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Amplitude (A):", None))
        self.fix_center.setText(QCoreApplication.translate("Form", u"Fixed", None))
        self.fix_sigma.setText(QCoreApplication.translate("Form", u"Fixed", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Sigma ( \u03c3 ):", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Min-Max:", None))
        self.fix_amp.setText(QCoreApplication.translate("Form", u"Fixed", None))
        self.label.setText(QCoreApplication.translate("Form", u"Center ( \u03bc ):", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Value:", None))
        self.pb_cent_mm.setText(QCoreApplication.translate("Form", u"Set", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Value:", None))
        self.bound_sigma.setText(QCoreApplication.translate("Form", u"Bound", None))
    # retranslateUi

