# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_QuizDialog.ui'
#
# Created: Sun Oct 29 01:58:35 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QuizDialog(object):
    def setupUi(self, QuizDialog):
        QuizDialog.setObjectName("QuizDialog")
        QuizDialog.resize(680, 378)
        self.gridLayout_2 = QtWidgets.QGridLayout(QuizDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelExpression = QtWidgets.QLabel(QuizDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelExpression.setFont(font)
        self.labelExpression.setObjectName("labelExpression")
        self.verticalLayout.addWidget(self.labelExpression)
        self.textEditExpression = QtWidgets.QTextEdit(QuizDialog)
        self.textEditExpression.setObjectName("textEditExpression")
        self.verticalLayout.addWidget(self.textEditExpression)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelMeaning = QtWidgets.QLabel(QuizDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelMeaning.setFont(font)
        self.labelMeaning.setObjectName("labelMeaning")
        self.verticalLayout_2.addWidget(self.labelMeaning)
        self.textEditMeaning = QtWidgets.QTextEdit(QuizDialog)
        self.textEditMeaning.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.textEditMeaning.setAcceptRichText(False)
        self.textEditMeaning.setObjectName("textEditMeaning")
        self.verticalLayout_2.addWidget(self.textEditMeaning)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.labelAlphaber = QtWidgets.QLabel(QuizDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelAlphaber.setFont(font)
        self.labelAlphaber.setObjectName("labelAlphaber")
        self.verticalLayout_4.addWidget(self.labelAlphaber)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widgetAlphabet = QtWidgets.QWidget(QuizDialog)
        self.widgetAlphabet.setMinimumSize(QtCore.QSize(0, 62))
        self.widgetAlphabet.setMaximumSize(QtCore.QSize(16777215, 62))
        self.widgetAlphabet.setObjectName("widgetAlphabet")
        self.gridLayout = QtWidgets.QGridLayout(self.widgetAlphabet)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setSpacing(2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.pushButton_01 = QtWidgets.QPushButton(self.widgetAlphabet)
        self.pushButton_01.setMinimumSize(QtCore.QSize(27, 27))
        self.pushButton_01.setMaximumSize(QtCore.QSize(27, 27))
        self.pushButton_01.setAutoDefault(False)
        self.pushButton_01.setObjectName("pushButton_01")
        self.verticalLayout_7.addWidget(self.pushButton_01)
        self.pushButton_02 = QtWidgets.QPushButton(self.widgetAlphabet)
        self.pushButton_02.setMinimumSize(QtCore.QSize(27, 27))
        self.pushButton_02.setMaximumSize(QtCore.QSize(27, 27))
        self.pushButton_02.setAutoDefault(False)
        self.pushButton_02.setObjectName("pushButton_02")
        self.verticalLayout_7.addWidget(self.pushButton_02)
        self.gridLayout.addLayout(self.verticalLayout_7, 0, 0, 1, 1)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pushButton_03 = QtWidgets.QPushButton(self.widgetAlphabet)
        self.pushButton_03.setMinimumSize(QtCore.QSize(27, 27))
        self.pushButton_03.setMaximumSize(QtCore.QSize(27, 27))
        self.pushButton_03.setAutoDefault(False)
        self.pushButton_03.setObjectName("pushButton_03")
        self.verticalLayout_6.addWidget(self.pushButton_03)
        self.pushButton_04 = QtWidgets.QPushButton(self.widgetAlphabet)
        self.pushButton_04.setMinimumSize(QtCore.QSize(27, 27))
        self.pushButton_04.setMaximumSize(QtCore.QSize(27, 27))
        self.pushButton_04.setAutoDefault(False)
        self.pushButton_04.setObjectName("pushButton_04")
        self.verticalLayout_6.addWidget(self.pushButton_04)
        self.gridLayout.addLayout(self.verticalLayout_6, 0, 1, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_05 = QtWidgets.QPushButton(self.widgetAlphabet)
        self.pushButton_05.setMinimumSize(QtCore.QSize(27, 27))
        self.pushButton_05.setMaximumSize(QtCore.QSize(27, 27))
        self.pushButton_05.setAutoDefault(False)
        self.pushButton_05.setObjectName("pushButton_05")
        self.verticalLayout_3.addWidget(self.pushButton_05)
        self.pushButton_06 = QtWidgets.QPushButton(self.widgetAlphabet)
        self.pushButton_06.setMinimumSize(QtCore.QSize(27, 27))
        self.pushButton_06.setMaximumSize(QtCore.QSize(27, 27))
        self.pushButton_06.setAutoDefault(False)
        self.pushButton_06.setObjectName("pushButton_06")
        self.verticalLayout_3.addWidget(self.pushButton_06)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 2, 1, 1)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setSpacing(2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pushButton_07 = QtWidgets.QPushButton(self.widgetAlphabet)
        self.pushButton_07.setMinimumSize(QtCore.QSize(27, 27))
        self.pushButton_07.setMaximumSize(QtCore.QSize(27, 27))
        self.pushButton_07.setAutoDefault(False)
        self.pushButton_07.setObjectName("pushButton_07")
        self.verticalLayout_8.addWidget(self.pushButton_07)
        self.pushButton_08 = QtWidgets.QPushButton(self.widgetAlphabet)
        self.pushButton_08.setMinimumSize(QtCore.QSize(27, 27))
        self.pushButton_08.setMaximumSize(QtCore.QSize(27, 27))
        self.pushButton_08.setAutoDefault(False)
        self.pushButton_08.setObjectName("pushButton_08")
        self.verticalLayout_8.addWidget(self.pushButton_08)
        self.gridLayout.addLayout(self.verticalLayout_8, 0, 3, 1, 1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButton_09 = QtWidgets.QPushButton(self.widgetAlphabet)
        self.pushButton_09.setMinimumSize(QtCore.QSize(27, 27))
        self.pushButton_09.setMaximumSize(QtCore.QSize(27, 27))
        self.pushButton_09.setAutoDefault(False)
        self.pushButton_09.setObjectName("pushButton_09")
        self.verticalLayout_5.addWidget(self.pushButton_09)
        self.pushButton_10 = QtWidgets.QPushButton(self.widgetAlphabet)
        self.pushButton_10.setMinimumSize(QtCore.QSize(27, 27))
        self.pushButton_10.setMaximumSize(QtCore.QSize(27, 27))
        self.pushButton_10.setAutoDefault(False)
        self.pushButton_10.setObjectName("pushButton_10")
        self.verticalLayout_5.addWidget(self.pushButton_10)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 4, 1, 1)
        self.horizontalLayout_2.addWidget(self.widgetAlphabet)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(142, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonCheck = QtWidgets.QPushButton(QuizDialog)
        self.pushButtonCheck.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonCheck.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/all/icons/ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonCheck.setIcon(icon)
        self.pushButtonCheck.setAutoDefault(False)
        self.pushButtonCheck.setObjectName("pushButtonCheck")
        self.horizontalLayout.addWidget(self.pushButtonCheck)
        self.pushButtonHint = QtWidgets.QPushButton(QuizDialog)
        self.pushButtonHint.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonHint.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/all/icons/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonHint.setIcon(icon1)
        self.pushButtonHint.setAutoDefault(False)
        self.pushButtonHint.setObjectName("pushButtonHint")
        self.horizontalLayout.addWidget(self.pushButtonHint)
        self.pushButtonCancel = QtWidgets.QPushButton(QuizDialog)
        self.pushButtonCancel.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonCancel.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/all/icons/cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonCancel.setIcon(icon2)
        self.pushButtonCancel.setAutoDefault(False)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 1)

        self.retranslateUi(QuizDialog)
        QtCore.QMetaObject.connectSlotsByName(QuizDialog)

    def retranslateUi(self, QuizDialog):
        _translate = QtCore.QCoreApplication.translate
        QuizDialog.setWindowTitle(_translate("QuizDialog", "Тест"))
        self.labelExpression.setText(_translate("QuizDialog", "Выражение:"))
        self.labelMeaning.setText(_translate("QuizDialog", "Значение:"))
        self.labelAlphaber.setText(_translate("QuizDialog", "Алфавит:"))
        self.pushButton_01.setText(_translate("QuizDialog", "Ä"))
        self.pushButton_02.setText(_translate("QuizDialog", "ä"))
        self.pushButton_03.setText(_translate("QuizDialog", "Å"))
        self.pushButton_04.setText(_translate("QuizDialog", "å"))
        self.pushButton_05.setText(_translate("QuizDialog", "Æ"))
        self.pushButton_06.setText(_translate("QuizDialog", "æ"))
        self.pushButton_07.setText(_translate("QuizDialog", "Ö"))
        self.pushButton_08.setText(_translate("QuizDialog", "ö"))
        self.pushButton_09.setText(_translate("QuizDialog", "Ø"))
        self.pushButton_10.setText(_translate("QuizDialog", "ø"))
        self.pushButtonCheck.setText(_translate("QuizDialog", "Проверить"))
        self.pushButtonHint.setText(_translate("QuizDialog", "Пропустить"))
        self.pushButtonCancel.setText(_translate("QuizDialog", "Закрыть"))

from gui.resources import Resources
