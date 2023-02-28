# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_exponential.ui'
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
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(492, 110)
        Form.setMinimumSize(QSize(0, 110))
        Form.setMaximumSize(QSize(16777215, 110))
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.group = QGroupBox(Form)
        self.group.setObjectName(u"group")
        self.group.setStyleSheet(u"#le_ampl_val, #le_decay_val{\n"
"font-weight: normal;\n"
"}")
        self.gridLayout = QGridLayout(self.group)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.group)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_4 = QLabel(self.group)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)

        self.label_2 = QLabel(self.group)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.le_ampl_val = QLineEdit(self.group)
        self.le_ampl_val.setObjectName(u"le_ampl_val")
        self.le_ampl_val.setMinimumSize(QSize(50, 0))
        self.le_ampl_val.setMaximumSize(QSize(50, 16777215))
        self.le_ampl_val.setReadOnly(True)

        self.gridLayout.addWidget(self.le_ampl_val, 0, 3, 1, 1)

        self.le_decay_val = QLineEdit(self.group)
        self.le_decay_val.setObjectName(u"le_decay_val")
        self.le_decay_val.setMinimumSize(QSize(50, 0))
        self.le_decay_val.setMaximumSize(QSize(50, 16777215))
        self.le_decay_val.setReadOnly(True)

        self.gridLayout.addWidget(self.le_decay_val, 1, 3, 1, 1)

        self.fix_ampl = QCheckBox(self.group)
        self.fix_ampl.setObjectName(u"fix_ampl")

        self.gridLayout.addWidget(self.fix_ampl, 0, 1, 1, 1)

        self.fix_decay = QCheckBox(self.group)
        self.fix_decay.setObjectName(u"fix_decay")

        self.gridLayout.addWidget(self.fix_decay, 1, 1, 1, 1)

        self.label_5 = QLabel(self.group)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)


        self.horizontalLayout.addWidget(self.group, 0, Qt.AlignLeft)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.group.setTitle(QCoreApplication.translate("Form", u"Exponential Function", None))
        self.label.setText(QCoreApplication.translate("Form", u"Amplitude (A):", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Value:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Decay ( \u03c4 ):", None))
        self.fix_ampl.setText(QCoreApplication.translate("Form", u"Fixed", None))
        self.fix_decay.setText(QCoreApplication.translate("Form", u"Fixed", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Value:", None))
    # retranslateUi

