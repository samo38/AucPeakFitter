# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainUi.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(779, 549)
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
"background-color: rgb(246, 243, 235);\n"
"}\n"
"#lineEdit, #lineEdit_2, #lineEdit_3, #lineEdit_4, #lineEdit_5, #lineEdit_6, #lineEdit_7{\n"
"font-weight: normal;\n"
"}")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frameT = QFrame(self.centralwidget)
        self.frameT.setObjectName(u"frameT")
        self.frameT.setMinimumSize(QSize(0, 60))
        self.frameT.setMaximumSize(QSize(16777215, 70))
        self.frameT.setFrameShape(QFrame.NoFrame)
        self.frameT.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frameT)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.frame_2 = QFrame(self.frameT)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(140, 0))
        self.frame_2.setMaximumSize(QSize(140, 16777215))
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 35))
        self.label_2.setMaximumSize(QSize(1000, 35))
        self.label_2.setAutoFillBackground(False)
        self.label_2.setStyleSheet(u"")
        self.label_2.setPixmap(QPixmap(u":/Icon/Resources/Icons/wave_packet_bg.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"Heebo"])
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label, 0, Qt.AlignTop)


        self.horizontalLayout.addWidget(self.frame_2)

        self.frame = QFrame(self.frameT)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setSpacing(1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 30))
        self.frame_3.setMaximumSize(QSize(16777215, 30))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.frame_3)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(130, 25))
        self.pushButton.setMaximumSize(QSize(130, 25))
        font1 = QFont()
        font1.setFamilies([u"Heebo"])
        font1.setBold(True)
        self.pushButton.setFont(font1)
        self.pushButton.setStyleSheet(u"background-color: rgb(135, 206, 235);\n"
"")
        icon = QIcon()
        icon.addFile(u":/Icon/Resources/Icons/file_open_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(25, 25))

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.label_4 = QLabel(self.frame_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.horizontalLayout_2.addWidget(self.label_4)

        self.lineEdit = QLineEdit(self.frame_3)
        self.lineEdit.setObjectName(u"lineEdit")
        font2 = QFont()
        font2.setFamilies([u"Heebo"])
        font2.setBold(False)
        self.lineEdit.setFont(font2)
        self.lineEdit.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.lineEdit)


        self.verticalLayout_3.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 30))
        self.frame_4.setMaximumSize(QSize(16777215, 30))
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.frame_4)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEdit_5 = QLineEdit(self.frame_4)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.horizontalLayout_3.addWidget(self.lineEdit_5)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_6)

        self.lineEdit_2 = QLineEdit(self.frame_4)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setFont(font2)
        self.lineEdit_2.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.lineEdit_2)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.lineEdit_6 = QLineEdit(self.frame_4)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.horizontalLayout_3.addWidget(self.lineEdit_6)

        self.label_10 = QLabel(self.frame_4)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_3.addWidget(self.label_10)

        self.lineEdit_7 = QLineEdit(self.frame_4)
        self.lineEdit_7.setObjectName(u"lineEdit_7")

        self.horizontalLayout_3.addWidget(self.lineEdit_7)

        self.label_7 = QLabel(self.frame_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_7)

        self.lineEdit_3 = QLineEdit(self.frame_4)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setFont(font2)
        self.lineEdit_3.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.lineEdit_3)

        self.label_8 = QLabel(self.frame_4)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_8)

        self.lineEdit_4 = QLineEdit(self.frame_4)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setFont(font2)
        self.lineEdit_4.setStyleSheet(u"")

        self.horizontalLayout_3.addWidget(self.lineEdit_4)


        self.verticalLayout_3.addWidget(self.frame_4)


        self.horizontalLayout.addWidget(self.frame)


        self.verticalLayout.addWidget(self.frameT)

        self.frameD = QFrame(self.centralwidget)
        self.frameD.setObjectName(u"frameD")
        self.frameD.setFrameShape(QFrame.NoFrame)
        self.frameD.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frameD)
        self.verticalLayout_4.setSpacing(1)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.frameD)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setSpacing(1)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.frame_5)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(200, 0))
        self.frame_7.setMaximumSize(QSize(200, 16777215))
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_9 = QFrame(self.frame_7)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMaximumSize(QSize(16777215, 16777215))
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.frame_9)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_5.addWidget(self.label_9)

        self.spinBox = QSpinBox(self.frame_9)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout_5.addWidget(self.spinBox)


        self.verticalLayout_6.addWidget(self.frame_9)

        self.groupBox = QGroupBox(self.frame_7)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.listWidget = QListWidget(self.groupBox)
        self.listWidget.setObjectName(u"listWidget")

        self.horizontalLayout_6.addWidget(self.listWidget)

        self.frame_10 = QFrame(self.groupBox)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(20, 42))
        self.frame_10.setMaximumSize(QSize(20, 42))
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_10)
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.pushButton_3 = QPushButton(self.frame_10)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(20, 20))
        self.pushButton_3.setMaximumSize(QSize(20, 20))
        self.pushButton_3.setStyleSheet(u"")
        icon1 = QIcon(QIcon.fromTheme(u"list-add"))
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QSize(20, 20))
        self.pushButton_3.setAutoRepeat(False)

        self.verticalLayout_5.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.frame_10)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(20, 20))
        self.pushButton_4.setMaximumSize(QSize(20, 20))
        self.pushButton_4.setStyleSheet(u"padding: 0px")
        icon2 = QIcon(QIcon.fromTheme(u"list-remove"))
        self.pushButton_4.setIcon(icon2)
        self.pushButton_4.setIconSize(QSize(20, 20))
        self.pushButton_4.setFlat(False)

        self.verticalLayout_5.addWidget(self.pushButton_4)


        self.horizontalLayout_6.addWidget(self.frame_10, 0, Qt.AlignTop)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.frame_11 = QFrame(self.frame_7)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(168, 25))
        self.frame_11.setMaximumSize(QSize(167, 25))
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_7.setSpacing(2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.pushButton_6 = QPushButton(self.frame_11)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setMinimumSize(QSize(20, 20))
        self.pushButton_6.setMaximumSize(QSize(20, 20))
        self.pushButton_6.setStyleSheet(u"background-color: rgb(249, 240, 107);")
        icon3 = QIcon()
        icon3.addFile(u":/Icon/Resources/Icons/tune_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_6.setIcon(icon3)
        self.pushButton_6.setIconSize(QSize(20, 20))

        self.horizontalLayout_7.addWidget(self.pushButton_6)

        self.pushButton_5 = QPushButton(self.frame_11)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(60, 25))
        self.pushButton_5.setMaximumSize(QSize(65, 25))
        self.pushButton_5.setStyleSheet(u"background-color: rgb(246, 97, 81);")
        icon4 = QIcon()
        icon4.addFile(u":/Icon/Resources/Icons/sprint_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_5.setIcon(icon4)
        self.pushButton_5.setIconSize(QSize(25, 25))

        self.horizontalLayout_7.addWidget(self.pushButton_5)

        self.pushButton_7 = QPushButton(self.frame_11)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setMinimumSize(QSize(80, 25))
        self.pushButton_7.setMaximumSize(QSize(80, 25))
        self.pushButton_7.setStyleSheet(u"background-color: rgb(143, 240, 164);")
        icon5 = QIcon()
        icon5.addFile(u":/Icon/Resources/Icons/text_snippet_FILL0_wght400_GRAD0_opsz48.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_7.setIcon(icon5)
        self.pushButton_7.setIconSize(QSize(25, 25))
        self.pushButton_7.setCheckable(False)

        self.horizontalLayout_7.addWidget(self.pushButton_7)


        self.verticalLayout_6.addWidget(self.frame_11)


        self.horizontalLayout_4.addWidget(self.frame_7)

        self.frame_8 = QFrame(self.frame_5)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_4.addWidget(self.frame_8)


        self.verticalLayout_4.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.frameD)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Raised)

        self.verticalLayout_4.addWidget(self.frame_6)


        self.verticalLayout.addWidget(self.frameD)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.pushButton_4.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"AUC Peak Decomposition Program", None))
        self.label_2.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"AUC Peak Decomposition", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Open AUC File", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"  Description:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Type:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u" Cell:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u" Channel:", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u" Wavelength:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u" RPM:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u" Temperature:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Scan Number:", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"List of Species", None))
        self.pushButton_3.setText("")
        self.pushButton_4.setText("")
        self.pushButton_6.setText("")
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Report", None))
    # retranslateUi

