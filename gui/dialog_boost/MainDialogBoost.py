#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import reprlib

from PyQt5.QtCore import Qt, QSettings,  QPoint, QEvent, pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QMessageBox, QDesktopWidget, QListWidgetItem, QFileDialog

from gui.dialog_boost.Ui_MainWindowBoost import Ui_MainWindowBoost
from gui.dialog_item_add.DialogItemAdd import DialogItemAdd
from gui.dialog_item_edit.DialogItemEdit import DialogItemEdit
from gui.quiz_dialog.DialogQuiz import DialogQuiz

from helpers.storage import Storage
from helpers.chance import mask_text


class Boost(QMainWindow, Ui_MainWindowBoost):
    HINTS_index_to_value = {}
    HINTS_index_to_value[0] = 0
    HINTS_index_to_value[1] = 0.7
    HINTS_index_to_value[2] = 0.8
    HINTS_index_to_value[3] = 0.9
    HINTS_index_to_value[4] = 1

    def __init__(self, boostPath):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.__boostPath = boostPath
        self.__storage = Storage()

        self.__customize()
        self.__loadSettings()

    def __customize(self):
        self.__createChildWidgets()
        self.__createContextMenus()
        self.__connectSignalsToSlots()
        self.__centerOnScreen()

        self.listWidgetExpressions.viewport().installEventFilter(self)

    def __createChildWidgets(self):
        self.__dialogItemAdd = DialogItemAdd(self)
        self.__dialogItemEdit = DialogItemEdit(self)
        self.__quizDialog = DialogQuiz(self)

    def __createContextMenus(self):
        self.listWidgetExpressions.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.listWidgetExpressions.setContextMenuPolicy(Qt.ActionsContextMenu) ???
        self.listWidgetExpressions.customContextMenuRequested.connect(self.__onListWidgetExpressionsContextMenuRequested)

        self.menuExpressionsPopup = QMenu(self)

        iconAdd = QIcon()
        iconAdd.addPixmap(QPixmap(":/all/icons/item_new.png"), QIcon.Normal, QIcon.Off)
        actionAddExpression = QAction(iconAdd, "Добавить", self.menuExpressionsPopup)

        iconEdit = QIcon()
        iconEdit.addPixmap(QPixmap(":/all/icons/item_edit.png"), QIcon.Normal, QIcon.Off)
        actionEditExpression = QAction(iconEdit, "Изменить", self.menuExpressionsPopup)

        iconDelete = QIcon()
        iconDelete.addPixmap(QPixmap(":/all/icons/item_delete.png"), QIcon.Normal, QIcon.Off)
        actionDeleteExpression = QAction(iconDelete, "Удалить", self.menuExpressionsPopup)

        actionAddExpression.triggered.connect(self.__onAddItemClicked)
        actionEditExpression.triggered.connect(self.__onEditItemClicked)
        actionDeleteExpression.triggered.connect(self.__onDeleteItemClicked)

        self.menuExpressionsPopup.addAction(actionAddExpression)
        self.menuExpressionsPopup.addAction(actionEditExpression)
        self.menuExpressionsPopup.addAction(actionDeleteExpression)

    def __connectSignalsToSlots(self):
        self.pushButtonAddItem.clicked.connect(self.__onAddItemClicked)
        self.pushButtonEditItem.clicked.connect(self.__onEditItemClicked)
        self.pushButtonDeleteItem.clicked.connect(self.__onDeleteItemClicked)

        self.listWidgetExpressions.currentRowChanged.connect(self.__onCurrentRowChanged)
        self.listWidgetExpressions.itemDoubleClicked.connect(self.__onItemDoubleClicked)

        self.__dialogItemAdd.emitItem.connect(self.__onAddItem)
        self.__dialogItemEdit.emitItem.connect(self.__onEditItem)

        self.__quizDialog.onDialogShown.connect(self.__onQuizDialogShown)
        self.__quizDialog.onDialogHidden.connect(self.__onQuizDialogHidden)

        self.actionNew.triggered.connect(self.__onActionNewTriggered)
        self.actionSave.triggered.connect(self.__onSaveActionTriggered)
        self.actionSaveAs.triggered.connect(self.__onSaveAsActionTriggered)
        self.actionOpen.triggered.connect(self.__onActionOpenTriggered)

        self.actionStart.triggered.connect(self.__onStartActionTriggered)
        self.actionExit.triggered.connect(self.__onActionExitTriggered)

    def __centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        x = (resolution.width() / 2) - (self.frameSize().width() / 2)
        y = (resolution.height() / 2) - (self.frameSize().height() / 2)
        self.move(x, y)

    def __mask(self):
        hint_index = self.comboBoxHint.currentIndex()
        hint_value = Boost.HINTS_index_to_value.get(hint_index, 0)

        self.listWidgetExpressions.clear()
        for expression in list(self.__storage.keys()):
            self.listWidgetExpressions.addItem(mask_text(expression, hint_value))

        meaning = self.textEditMeaning.toPlainText()
        meaning = mask_text(meaning, hint_value)
        self.textEditMeaning.setText(meaning)

    def __unmask(self):
        self.listWidgetExpressions.clear()

        expressions = list(self.__storage.keys())
        for expression in expressions:
            self.listWidgetExpressions.addItem(expression)

        expression = expressions[0]
        meaning = self.__storage[expression][0]
        self.textEditMeaning.setText(meaning)

    @pyqtSlot()
    def __onStartActionTriggered(self):
        hint_index = self.comboBoxHint.currentIndex()
        hint_value = Boost.HINTS_index_to_value.get(hint_index, 0)

        self.__quizDialog.hints = hint_value
        self.__quizDialog.shuffle = self.comboBoxShuffle.currentIndex()
        self.__quizDialog.storage = self.__storage
        self.__quizDialog.show()

    @pyqtSlot()
    def __onActionExitTriggered(self):
        self.close()

    @pyqtSlot()
    def __onQuizDialogShown(self):
        self.__mask()

    @pyqtSlot()
    def __onQuizDialogHidden(self):
        self.__unmask()

    @pyqtSlot(int)
    def __onCurrentRowChanged(self, currentRow):
        if -1 == currentRow:
            return

        row = self.listWidgetExpressions.item(currentRow)

        key = row.text()
        value, log = self.__storage.get(key, ("", []))

        self.textEditMeaning.setText(value)

    @pyqtSlot(QListWidgetItem)
    def __onItemDoubleClicked(self, item):
        expression = item.text()
        meaning = self.__storage[expression][0]

        self.__dialogItemEdit.setExpression(expression)
        self.__dialogItemEdit.setMeaning(meaning)
        self.__dialogItemEdit.show()

    @pyqtSlot(QPoint)
    def __onListWidgetExpressionsContextMenuRequested(self, point):
        self.menuExpressionsPopup.popup(self.listWidgetExpressions.viewport().mapToGlobal(point))

    @pyqtSlot()
    def __onAddItemClicked(self):
        self.__dialogItemAdd.show()

    @pyqtSlot(str, str)
    def __onAddItem(self, key, value):
        if key not in list(self.__storage.keys()):
            self.listWidgetExpressions.addItem(key)
        self.listWidgetExpressions.setCurrentItem(QListWidgetItem(key))
        self.setWindowTitle("Boost - {}*".format(reprlib.repr(self.__storage.path)[1:-1]))
        self.__storage[key] = value

    @pyqtSlot(str, str)
    def __onEditItem(self, key, value):
        newStorage = Storage(path=self.__storage.path)
        oldKey = self.__dialogItemEdit.expressionToChange

        if key in self.__storage.keys():
            for k, v in self.__storage.items():
                if k == key:
                    newStorage[k] = value
                else:
                    newStorage[k] = self.__storage[k]
        else:
            for k, v in self.__storage.items():
                if k == oldKey:
                    newStorage[key] = value
                else:
                    newStorage[k] = self.__storage[k]

        del self.__storage

        self.__storage = newStorage

        self.listWidgetExpressions.clear()
        self.listWidgetExpressions.addItems(self.__storage.keys())

        self.setWindowTitle("Boost - {}*".format(reprlib.repr(self.__storage.path)[1:-1]))

    @pyqtSlot()
    def __onEditItemClicked(self):
        currentRow = self.listWidgetExpressions.currentRow()
        key = self.listWidgetExpressions.item(currentRow).text()
        value = self.__storage[key][0]

        self.__dialogItemEdit.setExpression(key)
        self.__dialogItemEdit.setMeaning(value)

        self.__dialogItemEdit.pushButtonOk.setText("Изменить")
        self.__dialogItemEdit.show()

    @pyqtSlot()
    def __onDeleteItemClicked(self):
        row = self.listWidgetExpressions.currentRow()
        if -1 == row:
            return

        key = self.listWidgetExpressions.currentItem().text()
        if not key:
            return

        del self.__storage[key]

        self.listWidgetExpressions.clear()

        expressions = self.__storage.keys()
        if expressions:
            self.listWidgetExpressions.addItems(self.__storage.keys())

            previous_row = row - 1 if row > 0 else 0
            self.listWidgetExpressions.setCurrentRow(previous_row)
        else:
            self.textEditMeaning.clear()

        self.setWindowTitle("Boost - {}*".format(reprlib.repr(self.__storage.path)[1:-1]))

    @pyqtSlot()
    def __onActionNewTriggered(self):
        if self.__storage.is_dirty:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setWindowTitle('Внимание!')
            messageBox.setText('Файл {} был изменен! Сохранить изменения?'.format(reprlib.repr(self.__storage.path)))

            okButton = messageBox.addButton("Ok", QMessageBox.ActionRole)
            cancelButton = messageBox.addButton("Отмена", QMessageBox.ActionRole)

            messageBox.exec()
            if messageBox.clickedButton() == okButton:
                self.__saveStorage()

        self.listWidgetExpressions.clear()
        self.textEditMeaning.clear()
        self.setWindowTitle("Boost")

    @pyqtSlot()
    def __onSaveActionTriggered(self):
        self.__storage.dump()
        self.__saveSettings()
        self.setWindowTitle("Boost - {}".format(reprlib.repr(self.__storage.path)[1:-1]))

    @pyqtSlot()
    def __onSaveAsActionTriggered(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить как...", "", "*.boost")

        if path:
            self.__storage.dump(path)
            self.__saveSettings()

        self.setWindowTitle("Boost - {}".format(reprlib.repr(self.__storage.path)[1:-1]))

    @pyqtSlot()
    def __onActionOpenTriggered(self):
        if self.__storage.is_dirty:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setWindowTitle('Внимание!')
            messageBox.setText('Файл {} был изменен! Сохранить изменения?'.format(reprlib.repr(self.__storage.path)))

            okButton = messageBox.addButton("Ok", QMessageBox.ActionRole)
            cancelButton = messageBox.addButton("Отмена", QMessageBox.ActionRole)

            messageBox.exec()
            if messageBox.clickedButton() == okButton:
                self.__saveStorage()

        path, _ = QFileDialog.getOpenFileName(self, "Открыть...", "", "*.boost")
        if path:
            self.__loadStorage(path)

    def closeEvent(self, event):
        if self.__storage.is_dirty:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setWindowTitle('Внимание!')
            messageBox.setText('Файл {} был изменен! Сохранить изменения?'.format(reprlib.repr(self.__storage.path)))

            okButton = messageBox.addButton("Ok", QMessageBox.ActionRole)
            cancelButton = messageBox.addButton("Отмена", QMessageBox.ActionRole)

            messageBox.exec()
            if messageBox.clickedButton() == okButton:
                self.__saveStorage()

        self.__saveSettings()

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonDblClick:

            x = event.pos().x()
            y = event.pos().y()

            itemClicked = self.listWidgetExpressions.itemAt(x, y)
            if itemClicked:
                return QMainWindow.eventFilter(self, object, event)

            self.__dialogItemAdd.show()
            return True

        return QMainWindow.eventFilter(self, object, event)

    def __loadStorage(self, path):
        if not os.path.exists(path):
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowTitle('Ошибка!')
            messageBox.setText('Файл {} не найден!'.format(reprlib.repr(path)))
            messageBox.setStandardButtons(QMessageBox.Ok)
            okButton = messageBox.button(QMessageBox.Ok)
            okButton.setText("Ok")
            messageBox.exec()

            return

        self.__storage.clear()
        self.__storage.load(path)

        self.setWindowTitle("Boost - {}".format(reprlib.repr(path)[1:-1]))
        self.listWidgetExpressions.clear()
        self.textEditMeaning.clear()
        keys = self.__storage.keys()
        for key in keys:
            self.listWidgetExpressions.addItem(key)
        self.listWidgetExpressions.setCurrentRow(0)

    def __saveStorage(self, path=None):
        self.__storage.dump(path)

    def __createDefaultStorage(self, path):
        parentDirectoryPath = os.path.dirname(path)
        if not os.path.exists(parentDirectoryPath):
            os.mkdir(parentDirectoryPath)

        storage = Storage(path)
        storage["hello"] = "used to greet someone"
        storage.dump()

    def __loadSettings(self):
        settings = QSettings("RocketLabs", "Boost")

        hintIndex = settings.value("comboBoxHint_currentIndex", 0, type=int)
        self.comboBoxHint.setCurrentIndex(hintIndex)

        shuffleIndex = settings.value("comboboxShuffle_currentIndex", 0, type=int)
        self.comboBoxShuffle.setCurrentIndex(shuffleIndex)

        storagePath = settings.value("storagePath", "", type=str)

        if not storagePath:
            boost_directory = os.path.dirname(self.__boostPath)
            full_path = os.path.join(boost_directory, "dictionaries/hello.boost")

            if not os.path.exists(full_path):
                self.__createDefaultStorage(full_path)
            self.__loadStorage(full_path)

        elif not os.path.exists(storagePath):
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Critical)
            messageBox.setWindowTitle('Ошибка')
            messageBox.setText('Файл {} не найден!'.format(reprlib.repr(storagePath)))
            messageBox.setStandardButtons(QMessageBox.Ok)
            okButton = messageBox.button(QMessageBox.Ok)
            okButton.setText("Ok")
            messageBox.exec()

            boost_directory = os.path.dirname(self.__boostPath)
            full_path = os.path.join(boost_directory, "dictionaries/hello.boost")
            self.__createDefaultStorage(full_path)
            self.__loadStorage(full_path)

        else:
            self.__loadStorage(storagePath)

    def __saveSettings(self):
        settings = QSettings("RocketLabs", "Boost")
        settings.setValue("comboBoxHint_currentIndex", self.comboBoxHint.currentIndex())
        settings.setValue("comboboxShuffle_currentIndex", self.comboBoxShuffle.currentIndex())
        settings.setValue("storagePath", self.__storage.path)