from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton


class PushButton(QPushButton):
    """
    Custom button that emits mousePressed and mouseReleased events.
    """
    onMousePressed = pyqtSignal()
    onMouseReleased = pyqtSignal()

    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)

    def mousePressEvent(self, event):
        self.onMousePressed.emit()

    def mouseReleaseEvent(self, event):
        self.onMouseReleased.emit()


if "__main__" == __name__:

    import sys
    from PyQt5.QtWidgets import QApplication

    application = QApplication(sys.argv)

    pushButton = PushButton("Hello there")
    pushButton.show()

    sys.exit(application.exec_())
