from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFocusEvent, QTextCursor
from PyQt5.QtWidgets import QDialog, QPushButton

from gui.base.dialog_item.Ui_BaseDialogItem import Ui_BaseDialogItem


class BaseDialogItem(QDialog, Ui_BaseDialogItem):
    emitItem = pyqtSignal(str, str)

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.pushButtonOk.clicked.connect(self.__onPushButtonAddClicked)
        self.pushButtonCancel.clicked.connect(self.__onPushButtonCancelClicked)

        self.__customize()

    def __customize(self):
        self.__activeInputWidget = None
        self.textEditExpression.installEventFilter(self)
        self.textEditMeaning.installEventFilter(self)

        for widget in self.widgetAlphabet.children():
            if isinstance(widget, QPushButton):
                widget.clicked.connect(self.__onPushButtonMagicLetterClicked)

    def setExpression(self, text):
        self.textEditExpression.setText(text)

    def setMeaning(self, text):
        self.textEditMeaning.setText(text)

    def eventFilter(self, object, event):
        if QFocusEvent == type(event) and event.gotFocus():
            self.__activeInputWidget = object

        return False

    @pyqtSlot()
    def __onPushButtonMagicLetterClicked(self):
        letter = self.sender().text()

        cursor = self.__activeInputWidget.textCursor()
        cursor.insertText(letter)
        cursor.movePosition(QTextCursor.Right, 1)
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


if __name__ == "__main__":
    import sys

    from PyQt5.QtWidgets import QApplication

    application = QApplication(sys.argv)

    dialog = BaseDialogItem()
    dialog.show()

    sys.exit(application.exec_())
