from gui.base.dialog_item.BaseDialogItem import BaseDialogItem


class DialogItemAdd(BaseDialogItem):
    def __init__(self, parent=None):
        BaseDialogItem.__init__(self, parent)

        self.__customize()

    def __customize(self):
        self.setWindowTitle("Добавить")
        self.pushButtonOk.setText("Добавить")


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    application = QApplication(sys.argv)

    dialog = DialogItemAdd()
    dialog.show()

    sys.exit(application.exec_())
