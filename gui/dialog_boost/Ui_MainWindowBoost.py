# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_MainWindowBoost.ui'
#
# Created: Sat Aug  5 19:49:09 2017
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindowBoost(object):
    def setupUi(self, MainWindowBoost):
        MainWindowBoost.setObjectName("MainWindowBoost")
        MainWindowBoost.resize(1032, 481)
        self.centralwidget = QtWidgets.QWidget(MainWindowBoost)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(250, 0))
        self.frame.setMaximumSize(QtCore.QSize(400, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.labelExpressions = QtWidgets.QLabel(self.frame)
        self.labelExpressions.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelExpressions.setFont(font)
        self.labelExpressions.setObjectName("labelExpressions")
        self.gridLayout.addWidget(self.labelExpressions, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            109, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.pushButtonAddItem = QtWidgets.QPushButton(self.frame)
        self.pushButtonAddItem.setMinimumSize(QtCore.QSize(17, 17))
        self.pushButtonAddItem.setMaximumSize(QtCore.QSize(17, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonAddItem.setFont(font)
        self.pushButtonAddItem.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButtonAddItem.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/all/icons/item_new.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.pushButtonAddItem.setIcon(icon)
        self.pushButtonAddItem.setFlat(True)
        self.pushButtonAddItem.setObjectName("pushButtonAddItem")
        self.gridLayout.addWidget(self.pushButtonAddItem, 0, 2, 1, 1)
        self.pushButtonEditItem = QtWidgets.QPushButton(self.frame)
        self.pushButtonEditItem.setMinimumSize(QtCore.QSize(17, 17))
        self.pushButtonEditItem.setMaximumSize(QtCore.QSize(17, 17))
        self.pushButtonEditItem.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButtonEditItem.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/all/icons/item_edit.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.pushButtonEditItem.setIcon(icon1)
        self.pushButtonEditItem.setFlat(True)
        self.pushButtonEditItem.setObjectName("pushButtonEditItem")
        self.gridLayout.addWidget(self.pushButtonEditItem, 0, 3, 1, 1)
        self.pushButtonDeleteItem = QtWidgets.QPushButton(self.frame)
        self.pushButtonDeleteItem.setMinimumSize(QtCore.QSize(17, 17))
        self.pushButtonDeleteItem.setMaximumSize(QtCore.QSize(17, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonDeleteItem.setFont(font)
        self.pushButtonDeleteItem.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButtonDeleteItem.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/all/icons/item_delete.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.pushButtonDeleteItem.setIcon(icon2)
        self.pushButtonDeleteItem.setFlat(True)
        self.pushButtonDeleteItem.setObjectName("pushButtonDeleteItem")
        self.gridLayout.addWidget(self.pushButtonDeleteItem, 0, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            17, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem1, 0, 5, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelMeaning = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelMeaning.setFont(font)
        self.labelMeaning.setObjectName("labelMeaning")
        self.verticalLayout_2.addWidget(self.labelMeaning)
        self.textEditMeaning = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditMeaning.setMinimumSize(QtCore.QSize(0, 100))
        self.textEditMeaning.setMaximumSize(QtCore.QSize(16777215, 120))
        self.textEditMeaning.setReadOnly(True)
        self.textEditMeaning.setObjectName("textEditMeaning")
        self.verticalLayout_2.addWidget(self.textEditMeaning)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelHint = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelHint.setFont(font)
        self.labelHint.setObjectName("labelHint")
        self.verticalLayout.addWidget(self.labelHint)
        self.comboBoxHint = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxHint.setObjectName("comboBoxHint")
        self.comboBoxHint.addItem("")
        self.comboBoxHint.addItem("")
        self.comboBoxHint.addItem("")
        self.comboBoxHint.addItem("")
        self.comboBoxHint.addItem("")
        self.verticalLayout.addWidget(self.comboBoxHint)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.labelShuffle = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelShuffle.setFont(font)
        self.labelShuffle.setObjectName("labelShuffle")
        self.verticalLayout_4.addWidget(self.labelShuffle)
        self.comboBoxShuffle = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxShuffle.setObjectName("comboBoxShuffle")
        self.comboBoxShuffle.addItem("")
        self.comboBoxShuffle.addItem("")
        self.comboBoxShuffle.addItem("")
        self.verticalLayout_4.addWidget(self.comboBoxShuffle)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.labelOrder = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelOrder.setFont(font)
        self.labelOrder.setObjectName("labelOrder")
        self.verticalLayout_3.addWidget(self.labelOrder)
        self.comboBoxOrder = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxOrder.setObjectName("comboBoxOrder")
        self.comboBoxOrder.addItem("")
        self.comboBoxOrder.addItem("")
        self.comboBoxOrder.addItem("")
        self.verticalLayout_3.addWidget(self.comboBoxOrder)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem2)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 1, 2, 1)
        self.listWidgetExpressions = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.listWidgetExpressions.sizePolicy().hasHeightForWidth()
        )
        self.listWidgetExpressions.setSizePolicy(sizePolicy)
        self.listWidgetExpressions.setMaximumSize(QtCore.QSize(400, 16777215))
        self.listWidgetExpressions.setObjectName("listWidgetExpressions")
        self.gridLayout_2.addWidget(self.listWidgetExpressions, 1, 0, 1, 1)
        MainWindowBoost.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindowBoost)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1032, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuDictionary = QtWidgets.QMenu(self.menubar)
        self.menuDictionary.setObjectName("menuDictionary")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindowBoost.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindowBoost)
        self.statusbar.setObjectName("statusbar")
        MainWindowBoost.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindowBoost)
        self.toolBar.setObjectName("toolBar")
        MainWindowBoost.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew = QtWidgets.QAction(MainWindowBoost)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/all/icons/filenew.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.actionNew.setIcon(icon3)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindowBoost)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/all/icons/fileopen.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.actionOpen.setIcon(icon4)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindowBoost)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/all/icons/filesave.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.actionSave.setIcon(icon5)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtWidgets.QAction(MainWindowBoost)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/all/icons/filesaveas.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.actionSaveAs.setIcon(icon6)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionExit = QtWidgets.QAction(MainWindowBoost)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/all/icons/fileexit.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.actionExit.setIcon(icon7)
        self.actionExit.setObjectName("actionExit")
        self.actionStart = QtWidgets.QAction(MainWindowBoost)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/all/icons/run.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.actionStart.setIcon(icon8)
        self.actionStart.setObjectName("actionStart")
        self.actionAbout = QtWidgets.QAction(MainWindowBoost)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(
            QtGui.QPixmap(":/all/icons/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.actionAbout.setIcon(icon9)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuDictionary.addAction(self.actionStart)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDictionary.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSaveAs)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAbout)

        self.retranslateUi(MainWindowBoost)
        QtCore.QMetaObject.connectSlotsByName(MainWindowBoost)

    def retranslateUi(self, MainWindowBoost):
        _translate = QtCore.QCoreApplication.translate
        MainWindowBoost.setWindowTitle(_translate("MainWindowBoost", "Словарь"))
        self.labelExpressions.setText(_translate("MainWindowBoost", "Словарь:"))
        self.pushButtonAddItem.setToolTip(_translate("MainWindowBoost", "Добавить"))
        self.pushButtonEditItem.setToolTip(
            _translate("MainWindowBoost", "Редактировать")
        )
        self.pushButtonDeleteItem.setToolTip(_translate("MainWindowBoost", "Удалить"))
        self.labelMeaning.setText(_translate("MainWindowBoost", "Значение:"))
        self.labelHint.setText(_translate("MainWindowBoost", "Подсказки:"))
        self.comboBoxHint.setItemText(0, _translate("MainWindowBoost", "Нет"))
        self.comboBoxHint.setItemText(1, _translate("MainWindowBoost", "Мало"))
        self.comboBoxHint.setItemText(2, _translate("MainWindowBoost", "Средне"))
        self.comboBoxHint.setItemText(3, _translate("MainWindowBoost", "Много"))
        self.comboBoxHint.setItemText(4, _translate("MainWindowBoost", "Полностью"))
        self.labelShuffle.setText(_translate("MainWindowBoost", "Перебор:"))
        self.comboBoxShuffle.setItemText(0, _translate("MainWindowBoost", "По слову"))
        self.comboBoxShuffle.setItemText(
            1, _translate("MainWindowBoost", "По значению")
        )
        self.comboBoxShuffle.setItemText(2, _translate("MainWindowBoost", "Смешанный"))
        self.labelOrder.setText(_translate("MainWindowBoost", "Порядок:"))
        self.comboBoxOrder.setItemText(0, _translate("MainWindowBoost", "С начала"))
        self.comboBoxOrder.setItemText(1, _translate("MainWindowBoost", "С конца"))
        self.comboBoxOrder.setItemText(2, _translate("MainWindowBoost", "Случайный"))
        self.menuFile.setTitle(_translate("MainWindowBoost", "Файл"))
        self.menuDictionary.setTitle(_translate("MainWindowBoost", "Словарь"))
        self.menuHelp.setTitle(_translate("MainWindowBoost", "Помощь"))
        self.toolBar.setWindowTitle(_translate("MainWindowBoost", "toolBar"))
        self.actionNew.setText(_translate("MainWindowBoost", "Новый"))
        self.actionNew.setToolTip(_translate("MainWindowBoost", "Новый файл"))
        self.actionNew.setShortcut(_translate("MainWindowBoost", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindowBoost", "Открыть..."))
        self.actionOpen.setIconText(_translate("MainWindowBoost", "Открыть..."))
        self.actionOpen.setToolTip(_translate("MainWindowBoost", "Открыть файл..."))
        self.actionOpen.setShortcut(_translate("MainWindowBoost", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindowBoost", "Сохранить"))
        self.actionSave.setToolTip(_translate("MainWindowBoost", "Сохранить файл"))
        self.actionSave.setShortcut(_translate("MainWindowBoost", "Ctrl+S"))
        self.actionSaveAs.setText(_translate("MainWindowBoost", "Сохранить как..."))
        self.actionSaveAs.setIconText(_translate("MainWindowBoost", "Сохранить как..."))
        self.actionSaveAs.setToolTip(
            _translate("MainWindowBoost", "Сохранить файл как...")
        )
        self.actionExit.setText(_translate("MainWindowBoost", "Выход"))
        self.actionExit.setShortcut(_translate("MainWindowBoost", "Ctrl+Q"))
        self.actionStart.setText(_translate("MainWindowBoost", "Старт"))
        self.actionAbout.setText(_translate("MainWindowBoost", "О программе"))


from gui.resources import Resources
