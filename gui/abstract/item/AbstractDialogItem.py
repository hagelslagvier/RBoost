#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QTextCursor, QFocusEvent
from PyQt5.QtWidgets import QDialog

from gui.abstract.item.Ui_AbstractDialogItem import Ui_AbstractDialogItem


class AbstractDialogItem(QDialog, Ui_AbstractDialogItem):
    emitItem = pyqtSignal(str, str)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.pushButtonOk.clicked.connect(self.__onPushButtonAddClicked)
        self.pushButtonCancel.clicked.connect(self.__onPushButtonCancelClicked)

        self.__customize()

    def __customize(self):
        buttons = [self.pushButton_01, self.pushButton_02, self.pushButton_03, self.pushButton_04, self.pushButton_05, self.pushButton_06,
                   self.pushButton_07, self.pushButton_08, self.pushButton_09, self.pushButton_10, self.pushButton_11, self.pushButton_12]

        for button in buttons:
            button.clicked.connect(self.__onAlphabetButtonClicked)

        self.__activeInputWidget = None
        self.textEditExpression.installEventFilter(self)
        self.textEditMeaning.installEventFilter(self)

    def setExpression(self, text):
        self.textEditExpression.setText(text)

    def setMeaning(self, text):
        self.textEditMeaning.setText(text)

    def eventFilter(self, object, event):
        if QFocusEvent == type(event) and event.gotFocus():
            self.__activeInputWidget = object

        return False

    @pyqtSlot()
    def __onAlphabetButtonClicked(self):
        letter = self.sender().text()

        cursor = self.__activeInputWidget.textCursor()
        cursor.insertText(letter)
        cursor.movePosition(QTextCursor.Right, 1)
        # self.textEditMeaning.setTextCursor(cursor)
        self.__activeInputWidget.setFocus()

    @pyqtSlot()
    def __onPushButtonAddClicked(self):
        expression = self.textEditExpression.toPlainText()
        expression = str(expression).strip()
        if not expression:
            return

        meaning = self.textEditMeaning.toPlainText()
        meaning = str(meaning).strip()
        if not meaning:
            return

        self.emitItem.emit(expression, meaning)
        self.__onPushButtonCancelClicked()

    @pyqtSlot()
    def __onPushButtonCancelClicked(self):
        self.textEditExpression.clear()
        self.textEditMeaning.clear()
        self.hide()

if "__main__" == __name__:
    import sys
    from PyQt5.QtWidgets import QApplication

    application = QApplication(sys.argv)

    dialog = AbstractDialogItem()
    dialog.show()

    sys.exit(application.exec_())
