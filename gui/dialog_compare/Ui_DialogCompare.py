# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_DialogCompare.ui'
#
# Created: Sun Oct 29 01:59:57 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogCompare(object):
    def setupUi(self, DialogCompare):
        DialogCompare.setObjectName("DialogCompare")
        DialogCompare.resize(455, 378)
        self.gridLayout_2 = QtWidgets.QGridLayout(DialogCompare)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelCorrectAnswer = QtWidgets.QLabel(DialogCompare)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelCorrectAnswer.setFont(font)
        self.labelCorrectAnswer.setObjectName("labelCorrectAnswer")
        self.verticalLayout.addWidget(self.labelCorrectAnswer)
        self.textEditCorrectAnswer = QtWidgets.QTextEdit(DialogCompare)
        self.textEditCorrectAnswer.setObjectName("textEditCorrectAnswer")
        self.verticalLayout.addWidget(self.textEditCorrectAnswer)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelResult = QtWidgets.QLabel(DialogCompare)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelResult.setFont(font)
        self.labelResult.setObjectName("labelResult")
        self.verticalLayout_2.addWidget(self.labelResult)
        self.textEditUserAnswer = QtWidgets.QTextEdit(DialogCompare)
        self.textEditUserAnswer.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.textEditUserAnswer.setAcceptRichText(False)
        self.textEditUserAnswer.setObjectName("textEditUserAnswer")
        self.verticalLayout_2.addWidget(self.textEditUserAnswer)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(142, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonOk = QtWidgets.QPushButton(DialogCompare)
        self.pushButtonOk.setMinimumSize(QtCore.QSize(125, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonOk.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/all/icons/ok.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonOk.setIcon(icon)
        self.pushButtonOk.setAutoDefault(False)
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.horizontalLayout.addWidget(self.pushButtonOk)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 1)

        self.retranslateUi(DialogCompare)
        QtCore.QMetaObject.connectSlotsByName(DialogCompare)

    def retranslateUi(self, DialogCompare):
        _translate = QtCore.QCoreApplication.translate
        DialogCompare.setWindowTitle(_translate("DialogCompare", "Ошибки"))
        self.labelCorrectAnswer.setText(_translate("DialogCompare", "Правильный ответ:"))
        self.labelResult.setText(_translate("DialogCompare", "Результат:"))
        self.pushButtonOk.setText(_translate("DialogCompare", "Ok"))

from gui.resources import Resources
