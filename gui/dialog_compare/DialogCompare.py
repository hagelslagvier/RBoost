from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QDialog
from gui.dialog_compare.Ui_DialogCompare import Ui_DialogCompare


class DialogCompare(Ui_DialogCompare, QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setupUi(self)

        self.__customize()

    def __customize(self):
        self.textEditUserAnswer.installEventFilter(self)
        self.textEditCorrectAnswer.installEventFilter(self)

        self.pushButtonOk.clicked.connect(self.onPushButtonOkClicked)

    def eventFilter(self, receiver, event):
        if QEvent.KeyPress == event.type() and event.key() == Qt.Key_Return:
            self.pushButtonOk.click()

            return True

        return QDialog.eventFilter(self, receiver, event)

    def onPushButtonOkClicked(self):
        self.close()


if "__main__" == __name__:
    import sys
    from PyQt5.QtWidgets import QApplication

    application = QApplication(sys.argv)

    dialog = DialogCompare()
    dialog.show()

    sys.exit(application.exec_())