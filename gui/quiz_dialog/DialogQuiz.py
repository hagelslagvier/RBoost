from datetime import datetime
import random
from itertools import cycle
from random import randint, choice, seed

from PyQt5.QtCore import QEvent, Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFocusEvent, QTextCursor
from PyQt5.QtWidgets import QDialog

from core.diff import diff_match_patch
from core.events import event
from core.text import compare, mask_text
from gui.dialog_compare.DialogCompare import DialogCompare
from gui.quiz_dialog.Ui_DialogQuiz import Ui_DialogQuiz


class DialogQuiz(Ui_DialogQuiz, QDialog):
    onDialogShown = pyqtSignal()
    onDialogHidden = pyqtSignal()

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.__compareDialog = DialogCompare(self)

        self.hints = 0
        self.shuffle = 0
        self.order = 0
        self.repository = None
        self.index = 0
        self.picker = None

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(200)

        self.__customize()

    def __customize(self):
        self.__connectSignalsToSlots()

        self.__activeInputWidget = None
        self.textEditExpression.installEventFilter(self)
        self.textEditMeaning.installEventFilter(self)

    def __connectSignalsToSlots(self):
        alphabetButtons = [
            self.pushButton_01,
            self.pushButton_02,
            self.pushButton_03,
            self.pushButton_04,
            self.pushButton_05,
            self.pushButton_06,
            self.pushButton_07,
            self.pushButton_08,
            self.pushButton_09,
            self.pushButton_10,
            self.pushButton_11,
            self.pushButton_12,
        ]
        for button in alphabetButtons:
            button.clicked.connect(self.__onAlphabetButtonClicked)

        self.pushButtonCheck.clicked.connect(self.__onPushButtonCheckClicked)
        self.pushButtonHint.clicked.connect(self.__onPushButtonHintClicked)
        self.pushButtonCancel.clicked.connect(self.__onPushButtonCancelClicked)

        self.timer.timeout.connect(self.__onTimeout)

    def eventFilter(self, receiver, event):
        if QFocusEvent == type(event) and event.gotFocus():
            self.__activeInputWidget = receiver
            return False

        if QEvent.KeyPress == event.type() and event.key() == Qt.Key_Return:
            self.pushButtonCheck.click()
            return True

        return QDialog.eventFilter(self, receiver, event)

    def showEvent(self, showEvent):
        self.onDialogShown.emit()  # mask MainWindow

        checked_items = {
            index: key
            for index, (key, (_, is_checked)) in enumerate(self.repository.items())
            if is_checked
        }
        checked_indexes = list(checked_items.keys())

        def picker(keys):
            yield from cycle(keys)

        def random_picker(keys):
            random.seed(int(datetime.utcnow().timestamp()))
            while True:
                yield random.choice(keys)

        if 0 == self.order:
            self.index = 0

            self.picker = self.picker or picker(keys=sorted(checked_indexes, reverse=False))

        elif 1 == self.order:
            self.index = len(self.repository) - 1
            self.picker = self.picker or picker(keys=sorted(checked_indexes, reverse=True))

        else:
            self.index = randint(0, len(self.repository) - 1)
            self.picker = self.picker or random_picker(keys=checked_indexes)

        self.pick()


    def hideEvent(self, hideEvent):
        self.onDialogHidden.emit()
        # self.storage.dump()
        self.picker = None

    @pyqtSlot()
    def __onAlphabetButtonClicked(self):
        letter = self.sender().text()
        cursor = self.__activeInputWidget.textCursor()
        cursor.insertText(letter)
        cursor.movePosition(QTextCursor.Right, 1)
        self.__activeInputWidget.setFocus()

    @pyqtSlot()
    def __onPushButtonCheckClicked(self):
        key = list(self.repository.keys())[self.index]
        value = self.repository[key]

        expression = self.textEditExpression.toPlainText()
        meaning = self.textEditMeaning.toPlainText()

        if compare(key, expression) >= 95 and compare(value, meaning) >= 99:
            self.flashGreen()
            self.repository.commit_success_event(key=key)
        else:
            self.flashRed()
            self.repository.commit_failure_event(key=key)

            correct_answer = ""
            user_answer = ""
            if key != expression:
                correct_answer = key
                user_answer = expression

            if value != meaning:
                correct_answer = value
                user_answer = meaning

            self.__compareDialog.textEditCorrectAnswer.setHtml(correct_answer)
            DMP = diff_match_patch()
            diffs = DMP.diff_main(correct_answer, user_answer)
            html = DMP.diff_prettyHtml(diffs)
            self.__compareDialog.textEditUserAnswer.setHtml(html)
            self.__compareDialog.exec()

        self.next()
        self.pick()

    @pyqtSlot()
    def __onPushButtonHintClicked(self):
        key = list(self.repository.keys())[self.index]
        self.repository.commit_hint_event(key=key)
        self.flashYellow()

        self.next()
        self.pick()

    @pyqtSlot()
    def __onPushButtonCancelClicked(self):
        self.close()

    @pyqtSlot()
    def __onTimeout(self):
        self.__setColor((255, 255, 255))

    @pyqtSlot()
    def __onPushButtonStartStopRecordingMousePressed(self):
        print("Mouse pressed")

    @pyqtSlot()
    def __onPushButtonStartStopRecordingMouseReleased(self):
        print("Mouse released")

    def makeExpressionQuiz(self):
        keys = list(self.repository.keys())
        key = keys[next(self.picker)]

        value = self.repository[key]

        self.textEditMeaning.setText(value)
        self.textEditMeaning.setToolTip(mask_text(key, self.hints))
        self.textEditMeaning.setEnabled(False)

        self.textEditExpression.clear()
        self.textEditExpression.setToolTip("")
        self.textEditExpression.setEnabled(True)
        self.textEditExpression.setFocus()

    def makeMeaningQuiz(self):
        keys = list(self.repository.keys())
        key = keys[next(self.picker)]

        value = self.repository[key]

        self.textEditExpression.setText(key)
        self.textEditExpression.setToolTip(mask_text(value, self.hints))
        self.textEditExpression.setEnabled(False)

        self.textEditMeaning.clear()
        self.textEditMeaning.setToolTip("")
        self.textEditMeaning.setEnabled(True)
        self.textEditMeaning.setFocus()

    def pick(self):
        if 0 == self.shuffle:
            self.makeExpressionQuiz()
        elif 1 == self.shuffle:
            self.makeMeaningQuiz()
        else:
            if event(0.5):
                self.makeExpressionQuiz()
            else:
                self.makeMeaningQuiz()

    def next(self):
        checked_items = {
            index: key
            for index, (key, (_, is_checked)) in enumerate(self.repository.items())
            if is_checked
        }
        checked_indexes = list(checked_items.keys())

        def take_next(iterable):
            yield from cycle(iterable)

        keys = self.repository.keys()
        count = len(keys)

        def next_forward():
            found = False

            while not found:
                self.index += 1
                if self.index >= count:
                    self.index = 0

                key = keys[self.index]
                is_checked = self.repository.is_checked(key=key)
                if is_checked:
                    found = True

        def next_backward():
            found = False

            while not found:
                self.index -= 1
                if self.index < 0:
                    self.index = len(self.repository) - 1

                key = keys[self.index]
                is_checked = self.repository.is_checked(key=key)
                if is_checked:
                    found = True

        def next_random():
            found = False

            while not found:
                self.index = randint(0, count - 1)

                key = keys[self.index]
                is_checked = self.repository.is_checked(key=key)
                if is_checked:
                    found = True

        if 0 == self.order:
            next_forward()

        elif 1 == self.order:
            next_backward()

        else:
            next_random()

    def flashGreen(self):
        self.__setColor((139, 252, 113))
        self.timer.start()

    def flashYellow(self):
        self.__setColor((255, 204, 102))
        self.timer.start()

    def flashRed(self):
        self.__setColor((252, 113, 113))
        self.timer.start()

    def __setColor(self, color):
        for textEdit in [self.textEditExpression, self.textEditMeaning]:
            textEdit.setStyleSheet("background-color: rgb({}, {}, {});".format(*color))


if __name__ == "__main__":
    import sys

    from PyQt5.QtWidgets import QApplication

    application = QApplication(sys.argv)

    dialog = DialogQuiz()
    dialog.show()

    sys.exit(application.exec_())
