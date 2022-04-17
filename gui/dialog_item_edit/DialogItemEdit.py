from gui.base.dialog_item.BaseDialogItem import BaseDialogItem


class DialogItemEdit(BaseDialogItem):
    def __init__(self, parent=None):
        BaseDialogItem.__init__(self, parent)
        self.expressionToChange = None

        self.__customize()

    def __customize(self):
        self.setWindowTitle("Изменить")
        self.pushButtonOk.setText("Изменить")

    def setExpression(self, text):
        self.expressionToChange = text
        BaseDialogItem.setExpression(self, text)

    def hideEvent(self, event):
        self.textEditExpression.clear()
        self.textEditMeaning.clear()


if __name__ == "__main__":
    import sys

    from PyQt5.QtWidgets import QApplication

    application = QApplication(sys.argv)

    dialog = DialogItemEdit()
    dialog.show()

    sys.exit(application.exec_())
