#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from gui.dialog_compare.Ui_DialogCompare import Ui_DialogCompare


class DialogCompare(Ui_DialogCompare, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setupUi(self)
        self.pushButtonOk.clicked.connect(self.onPushButtonOkClicked)

    def onPushButtonOkClicked(self):
        self.close()


if "__main__" == __name__:
    import sys
    from PyQt5.QtWidgets import QApplication

    application = QApplication(sys.argv)

    dialog = DialogCompare()
    dialog.show()

    sys.exit(application.exec_())