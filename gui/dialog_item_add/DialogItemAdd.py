#!/usr/bin/python
# -*- coding: utf-8 -*-

from gui.abstract.item.AbstractDialogItem import AbstractDialogItem


class DialogItemAdd(AbstractDialogItem):
    def __init__(self, parent=None):
        AbstractDialogItem.__init__(self, parent)

        self.__customize()

    def __customize(self):
        self.setWindowTitle("Добавить")
        self.pushButtonOk.setText("Добавить")


if "__main__" == __name__:
    import sys
    from PyQt5.QtWidgets import QApplication

    application = QApplication(sys.argv)

    dialog = DialogItemAdd()
    dialog.show()

    sys.exit(application.exec_())
