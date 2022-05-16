from pathlib import Path
from typing import Optional

from PyQt5.QtCore import QEvent, QPoint, QSettings, Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QDesktopWidget,
    QFileDialog,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMessageBox,
)

from core.repository.storage import Repository
from core.text import mask_text
from gui.dialog_boost.Ui_MainWindowBoost import Ui_MainWindowBoost
from gui.dialog_item_add.DialogItemAdd import DialogItemAdd
from gui.dialog_item_edit.DialogItemEdit import DialogItemEdit
from gui.quiz_dialog.DialogQuiz import DialogQuiz


class Boost(QMainWindow, Ui_MainWindowBoost):
    HINTS_index_to_value = {}
    HINTS_index_to_value[0] = 0
    HINTS_index_to_value[1] = 0.7
    HINTS_index_to_value[1] = 0.7
    HINTS_index_to_value[2] = 0.8
    HINTS_index_to_value[3] = 0.9
    HINTS_index_to_value[4] = 1

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.__customize()
        self.__loadSettings()

    def __customize(self):
        self.__createChildWidgets()
        self.__createContextMenus()
        self.__connectSignalsToSlots()
        self.__installEventFilters()
        self.__centerOnScreen()

    def __createChildWidgets(self):
        self.__dialogItemAdd = DialogItemAdd(self)
        self.__dialogItemEdit = DialogItemEdit(self)
        self.__dialogQuiz = DialogQuiz(self)

    def __createContextMenus(self):
        self.listWidgetExpressions.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidgetExpressions.customContextMenuRequested.connect(
            self.__onListWidgetExpressionsContextMenuRequested
        )

        self.menuExpressionsPopup = QMenu(self)

        iconAdd = QIcon()
        iconAdd.addPixmap(QPixmap(":/all/icons/item_new.png"), QIcon.Normal, QIcon.Off)
        actionAddExpression = QAction(iconAdd, "Добавить", self.menuExpressionsPopup)

        iconEdit = QIcon()
        iconEdit.addPixmap(
            QPixmap(":/all/icons/item_edit.png"), QIcon.Normal, QIcon.Off
        )
        actionEditExpression = QAction(iconEdit, "Изменить", self.menuExpressionsPopup)

        iconDelete = QIcon()
        iconDelete.addPixmap(
            QPixmap(":/all/icons/item_delete.png"), QIcon.Normal, QIcon.Off
        )
        actionDeleteExpression = QAction(
            iconDelete, "Удалить", self.menuExpressionsPopup
        )

        actionAddExpression.triggered.connect(self.__onAddItemClicked)
        actionEditExpression.triggered.connect(self.__onEditItemClicked)
        actionDeleteExpression.triggered.connect(self.__onDeleteItemClicked)

        self.menuExpressionsPopup.addAction(actionAddExpression)
        self.menuExpressionsPopup.addAction(actionEditExpression)
        self.menuExpressionsPopup.addAction(actionDeleteExpression)

    def __connectSignalsToSlots(self):
        self.pushButtonAddItem.clicked.connect(self.__onAddItemClicked)
        self.pushButtonEditItem.clicked.connect(self.__onEditItemClicked)
        self.pushButtonDeleteItem.clicked.connect(self.__onDeleteItemClicked)

        self.listWidgetExpressions.currentRowChanged.connect(self.__onCurrentRowChanged)
        self.listWidgetExpressions.itemDoubleClicked.connect(self.__onItemDoubleClicked)

        self.__dialogItemAdd.emitItem.connect(self.__onAddItem)
        self.__dialogItemEdit.emitItem.connect(self.__onEditItem)

        self.__dialogQuiz.onDialogShown.connect(self.__onQuizDialogShown)
        self.__dialogQuiz.onDialogHidden.connect(self.__onQuizDialogHidden)

        self.actionNew.triggered.connect(self.__onActionNewTriggered)
        self.actionSave.triggered.connect(self.__onSaveActionTriggered)
        self.actionSaveAs.triggered.connect(self.__onSaveAsActionTriggered)
        self.actionOpen.triggered.connect(self.__onActionOpenTriggered)

        self.actionStart.triggered.connect(self.__onStartActionTriggered)
        self.actionExit.triggered.connect(self.__onActionExitTriggered)

    def __installEventFilters(self):
        self.listWidgetExpressions.viewport().installEventFilter(self)

    def __centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        x = (resolution.width() / 2) - (self.frameSize().width() / 2)
        y = (resolution.height() / 2) - (self.frameSize().height() / 2)
        self.move(x, y)

    def __mask(self):
        hint_index = self.comboBoxHint.currentIndex()
        hint_value = Boost.HINTS_index_to_value.get(hint_index, 0)

        self.listWidgetExpressions.clear()
        for expression in self.__repository.keys():
            self.listWidgetExpressions.addItem(mask_text(expression, hint_value))

        meaning = self.textEditMeaning.toPlainText()
        meaning = mask_text(meaning, hint_value)
        self.textEditMeaning.setText(meaning)

    def __unmask(self):
        self.listWidgetExpressions.clear()

        keys = self.__repository.keys()
        for key in keys:
            self.listWidgetExpressions.addItem(key)

        first_key = keys[0]
        self.listWidgetExpressions.setCurrentRow(0)
        meaning = self.__repository[first_key]
        self.textEditMeaning.setText(meaning)

    @pyqtSlot()
    def __onStartActionTriggered(self):
        hint_index = self.comboBoxHint.currentIndex()
        hint_value = Boost.HINTS_index_to_value.get(hint_index, 0)

        self.__dialogQuiz.hints = hint_value
        self.__dialogQuiz.shuffle = self.comboBoxShuffle.currentIndex()
        self.__dialogQuiz.order = self.comboBoxOrder.currentIndex()
        self.__dialogQuiz.storage = self.__repository
        self.__dialogQuiz.show()

    @pyqtSlot()
    def __onActionExitTriggered(self):
        self.close()

    @pyqtSlot()
    def __onQuizDialogShown(self):
        self.__mask()

    @pyqtSlot()
    def __onQuizDialogHidden(self):
        self.__unmask()

    @pyqtSlot(int)
    def __onCurrentRowChanged(self, currentRow):
        if -1 == currentRow:
            return

        row = self.listWidgetExpressions.item(currentRow)

        key = row.text()
        value = self.__repository[key]

        self.textEditMeaning.setText(value)

    @pyqtSlot(QListWidgetItem)
    def __onItemDoubleClicked(self, item):
        expression = item.text()
        meaning = self.__repository[expression]

        self.__dialogItemEdit.setExpression(expression)
        self.__dialogItemEdit.setMeaning(meaning)
        self.__dialogItemEdit.show()

    @pyqtSlot(QPoint)
    def __onListWidgetExpressionsContextMenuRequested(self, point):
        self.menuExpressionsPopup.popup(
            self.listWidgetExpressions.viewport().mapToGlobal(point)
        )

    @pyqtSlot()
    def __onAddItemClicked(self):
        self.__dialogItemAdd.show()

    @pyqtSlot(str, str)
    def __onAddItem(self, key, value):
        if key in self.__repository.keys():
            return

        self.__repository[key] = value

        self.listWidgetExpressions.addItem(key)
        self.listWidgetExpressions.setCurrentItem(QListWidgetItem(key))

        self.setWindowTitle("Boost - {}*".format(self.__repository.path))

    @pyqtSlot(str, str)
    def __onEditItem(self, key, value):
        self.__repository[key] = value

        current_key = self.listWidgetExpressions.currentItem()

        if key != current_key:
            self.listWidgetExpressions.clear()
            self.listWidgetExpressions.addItems(self.__repository.keys())
        else:
            self.textEditMeaning.setText(value)

        self.setWindowTitle("Boost - {}*".format(self.__repository.path))

    @pyqtSlot()
    def __onEditItemClicked(self):
        currentRow = self.listWidgetExpressions.currentRow()
        key = self.listWidgetExpressions.item(currentRow).text()
        value = self.__repository[key]

        self.__dialogItemEdit.setExpression(key)
        self.__dialogItemEdit.setMeaning(value)

        self.__dialogItemEdit.pushButtonOk.setText("Изменить")
        self.__dialogItemEdit.show()

    @pyqtSlot()
    def __onDeleteItemClicked(self):
        row = self.listWidgetExpressions.currentRow()
        if -1 == row:
            return

        key = self.listWidgetExpressions.currentItem().text()
        if not key:
            return

        if not self.__repository.is_dirty:
            self.__repository.save(path=f"{self.__repository.path}.backup")

        del self.__repository[key]

        self.listWidgetExpressions.clear()

        expressions = self.__repository.keys()
        if expressions:
            self.listWidgetExpressions.addItems(self.__repository.keys())

            previous_row = row - 1 if row > 0 else 0
            self.listWidgetExpressions.setCurrentRow(previous_row)
        else:
            self.textEditMeaning.clear()

        self.setWindowTitle("Boost - {}*".format(self.__repository.path))

    @pyqtSlot()
    def __onActionNewTriggered(self):
        if self.__repository.is_dirty:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Question)
            message_box.setWindowTitle("Внимание!")
            message_box.setText(
                "Файл {} был изменен! Сохранить изменения?".format(
                    self.__repository.path
                )
            )

            ok_button = message_box.addButton("Ok", QMessageBox.ActionRole)
            cancel_button = message_box.addButton("Отмена", QMessageBox.ActionRole)

            message_box.exec()
            if message_box.clickedButton() == ok_button:
                self.__saveRepository()
            else:
                self.__restoreRepository()

        home_directory = Path(__file__).resolve().parents[2]
        default_path = home_directory / "dictionaries/new.db"
        self.__repository = Repository(path=str(default_path))

        self.listWidgetExpressions.clear()
        self.textEditMeaning.clear()
        self.setWindowTitle("Boost - {}*".format(self.__repository.path))

    @pyqtSlot()
    def __onSaveActionTriggered(self):
        self.__saveRepository()
        self.__saveSettings()
        self.setWindowTitle("Boost - {}".format(self.__repository.path))

    @pyqtSlot()
    def __onSaveAsActionTriggered(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить как...", "", "*.db")

        if not path:
            return

        if not str(path).endswith(".db"):
            path += ".db"

        self.__saveRepository(path=path)
        self.__saveSettings()

        self.setWindowTitle("Boost - {}".format(self.__repository.path))

    @pyqtSlot()
    def __onActionOpenTriggered(self):
        if self.__repository.is_dirty:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setWindowTitle("Внимание!")
            messageBox.setText(
                "Файл {} был изменен! Сохранить изменения?".format(
                    self.__repository.path
                )
            )

            okButton = messageBox.addButton("Ok", QMessageBox.ActionRole)
            cancelButton = messageBox.addButton("Отмена", QMessageBox.ActionRole)

            messageBox.exec()
            if messageBox.clickedButton() == okButton:
                self.__saveRepository()

        path, _ = QFileDialog.getOpenFileName(self, "Открыть...", "", "*.db")
        if path:
            self.__loadRepository(path)

    def closeEvent(self, event):
        if self.__repository.is_dirty:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setWindowTitle("Внимание!")
            messageBox.setText(
                "Файл {} был изменен! Сохранить изменения?".format(
                    self.__repository.path
                )
            )

            okButton = messageBox.addButton("Ok", QMessageBox.ActionRole)
            cancelButton = messageBox.addButton("Отмена", QMessageBox.ActionRole)

            messageBox.exec()
            if messageBox.clickedButton() == okButton:
                self.__saveRepository()

        self.__saveSettings()

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonDblClick:
            x = event.pos().x()
            y = event.pos().y()

            item_clicked = self.listWidgetExpressions.itemAt(x, y)
            if item_clicked:
                return QMainWindow.eventFilter(self, object, event)

            self.__dialogItemAdd.show()

            return True

        return QMainWindow.eventFilter(self, object, event)

    def __loadRepository(self, path: str):
        if not Path(path).is_file():
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Critical)
            message_box.setWindowTitle("Ошибка!")
            message_box.setText("Файл {} не найден!".format(reprlib.repr(path)))
            message_box.setStandardButtons(QMessageBox.Ok)
            ok_button = message_box.button(QMessageBox.Ok)
            ok_button.setText("Ok")
            message_box.exec()

            return

        self.__repository = Repository(path=path)

        self.setWindowTitle("Boost - {}".format(path))
        self.listWidgetExpressions.clear()
        self.textEditMeaning.clear()

        for key in self.__repository.keys():
            self.listWidgetExpressions.addItem(key)

        self.listWidgetExpressions.setCurrentRow(0)

    def __saveRepository(self, path: Optional[str] = None):
        self.__repository.save(path=path)

    def __restoreRepository(self):
        self.__repository.restore()

    def __createDefaultRepository(self, path: str):
        default_repository = Repository(path=path)
        default_repository["hello"] = "used to greet someone"

    def __loadSettings(self):
        settings = QSettings("RocketLabs", "Boost")

        hint_index = settings.value("comboBoxHint_currentIndex", 0, type=int)
        self.comboBoxHint.setCurrentIndex(hint_index)

        shuffle_index = settings.value("comboboxShuffle_currentIndex", 0, type=int)
        self.comboBoxShuffle.setCurrentIndex(shuffle_index)

        order_index = settings.value("comboboxOrder_currentIndex", 0, type=int)
        self.comboBoxOrder.setCurrentIndex(order_index)

        repository_path = settings.value("repositoryPath", "", type=str)
        if not repository_path:
            home_directory = Path(__file__).resolve().parents[2]
            default_path = home_directory / "dictionaries/hello.db"

            Path(default_path).unlink(missing_ok=True)

            self.__createDefaultRepository(path=str(default_path))
            self.__loadRepository(path=str(default_path))

        elif not Path(repository_path).is_file():
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Critical)
            message_box.setWindowTitle("Ошибка")
            message_box.setText(
                "Файл {} не найден!".format(reprlib.repr(repository_path))
            )
            message_box.setStandardButtons(QMessageBox.Ok)
            ok_button = message_box.button(QMessageBox.Ok)
            ok_button.setText("Ok")
            message_box.exec()

            home_directory = Path(__file__).resolve().parents[2]
            default_path = home_directory / "dictionaries/hello.db"

            self.__createDefaultRepository(path=str(default_path))
            self.__loadRepository(path=str(default_path))

        else:
            self.__loadRepository(path=str(repository_path))

    def __saveSettings(self):
        settings = QSettings("RocketLabs", "Boost")
        settings.setValue("comboBoxHint_currentIndex", self.comboBoxHint.currentIndex())
        settings.setValue(
            "comboboxShuffle_currentIndex", self.comboBoxShuffle.currentIndex()
        )
        settings.setValue(
            "comboboxOrder_currentIndex", self.comboBoxOrder.currentIndex()
        )
        settings.setValue("repositoryPath", str(self.__repository.path))
