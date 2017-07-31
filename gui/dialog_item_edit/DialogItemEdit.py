#!/usr/bin/python
# -*- coding: utf-8 -*-

from gui.abstract.item.AbstractDialogItem import AbstractDialogItem


class DialogItemEdit(AbstractDialogItem):
    def __init__(self, parent=None):
        AbstractDialogItem.__init__(self, parent)
        self.expressionToChange = None

        self.__customize()

    def __customize(self):
        self.setWindowTitle("Изменить")
        self.pushButtonOk.setText("Изменить")

    def setExpression(self, text):
        self.expressionToChange = text
        AbstractDialogItem.setExpression(self, text)

    def hideEvent(self, event):
        self.textEditExpression.clear()
        self.textEditMeaning.clear()


if "__main__" == __name__:
    import sys
    from PyQt5.QtWidgets import QApplication

    application = QApplication(sys.argv)

    dialog = DialogItemEdit()
    dialog.show()

    sys.exit(application.exec_())
