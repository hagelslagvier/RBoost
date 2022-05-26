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

from core.repository.repository import Repository
from core.text import mask_text
from gui.dialog_boost.Ui_MainWindowBoost import Ui_MainWindowBoost
from gui.dialog_item_add.DialogItemAdd import DialogItemAdd
from gui.dialog_item_edit.DialogItemEdit import DialogItemEdit
from gui.quiz_dialog.DialogQuiz import DialogQuiz


class Boost(QMainWindow, Ui_MainWindowBoost):
    HINTS_INDEX_TO_VALUE_MAP = {}
    HINTS_INDEX_TO_VALUE_MAP[0] = 0
    HINTS_INDEX_TO_VALUE_MAP[1] = 0.7
    HINTS_INDEX_TO_VALUE_MAP[1] = 0.7
    HINTS_INDEX_TO_VALUE_MAP[2] = 0.8
    HINTS_INDEX_TO_VALUE_MAP[3] = 0.9
    HINTS_INDEX_TO_VALUE_MAP[4] = 1

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.customize()
        self.loadSettings()

    def customize(self):
        self.createChildWidgets()
        self.createContextMenus()
        self.connectSignalsToSlots()
        self.installEventFilters()
        self.centerOnScreen()

    def createChildWidgets(self):
        self.dialogItemAdd = DialogItemAdd(self)
        self.dialogItemEdit = DialogItemEdit(self)
        self.dialogQuiz = DialogQuiz(self)

    def createContextMenus(self):
        self.listWidgetExpressions.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidgetExpressions.customContextMenuRequested.connect(
            self.onListWidgetExpressionsContextMenuRequested
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

        actionAddExpression.triggered.connect(self.onAddItemClicked)
        actionEditExpression.triggered.connect(self.onEditItemClicked)
        actionDeleteExpression.triggered.connect(self.onDeleteItemClicked)

        self.menuExpressionsPopup.addAction(actionAddExpression)
        self.menuExpressionsPopup.addAction(actionEditExpression)
        self.menuExpressionsPopup.addAction(actionDeleteExpression)

    def connectSignalsToSlots(self):
        self.pushButtonAddItem.clicked.connect(self.onAddItemClicked)
        self.pushButtonEditItem.clicked.connect(self.onEditItemClicked)
        self.pushButtonDeleteItem.clicked.connect(self.onDeleteItemClicked)

        self.listWidgetExpressions.currentRowChanged.connect(self.onCurrentRowChanged)
        self.listWidgetExpressions.itemDoubleClicked.connect(self.onItemDoubleClicked)

        self.dialogItemAdd.emitItem.connect(self.onAddItem)
        self.dialogItemEdit.emitItem.connect(self.onEditItem)

        self.dialogQuiz.onDialogShown.connect(self.onQuizDialogShown)
        self.dialogQuiz.onDialogHidden.connect(self.onQuizDialogHidden)

        self.actionNew.triggered.connect(self.onActionNewTriggered)
        self.actionSave.triggered.connect(self.onSaveActionTriggered)
        self.actionSaveAs.triggered.connect(self.onSaveAsActionTriggered)
        self.actionOpen.triggered.connect(self.onActionOpenTriggered)

        self.actionStart.triggered.connect(self.onStartActionTriggered)
        self.actionExit.triggered.connect(self.onActionExitTriggered)

    def installEventFilters(self):
        self.listWidgetExpressions.viewport().installEventFilter(self)

    def centerOnScreen(self):
        resolution = QDesktopWidget().screenGeometry()
        x = (resolution.width() / 2) - (self.frameSize().width() / 2)
        y = (resolution.height() / 2) - (self.frameSize().height() / 2)
        self.move(x, y)

    def maskContent(self):
        hint_index = self.comboBoxHint.currentIndex()
        hint_value = Boost.HINTS_INDEX_TO_VALUE_MAP.get(hint_index, 0)

        self.listWidgetExpressions.clear()
        for expression in self.repository.keys():
            self.listWidgetExpressions.addItem(mask_text(expression, hint_value))

        meaning = self.textEditMeaning.toPlainText()
        meaning = mask_text(meaning, hint_value)
        self.textEditMeaning.setText(meaning)

    def unmaskContent(self):
        self.listWidgetExpressions.clear()

        keys = self.repository.keys()
        for key in keys:
            self.listWidgetExpressions.addItem(key)

        first_key = keys[0]
        self.listWidgetExpressions.setCurrentRow(0)
        meaning = self.repository[first_key]
        self.textEditMeaning.setText(meaning)

    @pyqtSlot()
    def onStartActionTriggered(self):
        hint_index = self.comboBoxHint.currentIndex()
        hint_value = Boost.HINTS_INDEX_TO_VALUE_MAP.get(hint_index, 0)

        self.dialogQuiz.hints = hint_value
        self.dialogQuiz.shuffle = self.comboBoxShuffle.currentIndex()
        self.dialogQuiz.order = self.comboBoxOrder.currentIndex()
        self.dialogQuiz.repository = self.repository
        self.dialogQuiz.show()

    @pyqtSlot()
    def onActionExitTriggered(self):
        self.close()

    @pyqtSlot()
    def onQuizDialogShown(self):
        self.maskContent()

    @pyqtSlot()
    def onQuizDialogHidden(self):
        self.unmaskContent()

    @pyqtSlot(int)
    def onCurrentRowChanged(self, currentRow):
        if -1 == currentRow:
            return

        row = self.listWidgetExpressions.item(currentRow)

        key = row.text()
        value = self.repository[key]

        self.textEditMeaning.setText(value)

    @pyqtSlot(QListWidgetItem)
    def onItemDoubleClicked(self, item):
        expression = item.text()
        meaning = self.repository[expression]

        self.dialogItemEdit.setExpression(expression)
        self.dialogItemEdit.setMeaning(meaning)
        self.dialogItemEdit.show()

    @pyqtSlot(QPoint)
    def onListWidgetExpressionsContextMenuRequested(self, point):
        self.menuExpressionsPopup.popup(
            self.listWidgetExpressions.viewport().mapToGlobal(point)
        )

    @pyqtSlot()
    def onAddItemClicked(self):
        self.dialogItemAdd.show()

    @pyqtSlot(str, str)
    def onAddItem(self, key, value):
        if key in self.repository.keys():
            return

        self.repository[key] = value

        self.listWidgetExpressions.addItem(key)
        self.listWidgetExpressions.setCurrentItem(QListWidgetItem(key))

        self.setWindowTitle("Boost - {}*".format(self.repository.path))

    @pyqtSlot(str, str)
    def onEditItem(self, new_key: str, new_value: str) -> None:
        current_row = self.listWidgetExpressions.currentRow()
        current_item = self.listWidgetExpressions.currentItem()
        current_key = current_item.text()
        self.listWidgetExpressions.takeItem(current_row)

        del self.repository[current_key]
        self.repository[new_key] = new_value

        self.listWidgetExpressions.insertItem(current_row, new_key)
        self.listWidgetExpressions.setCurrentRow(current_row)
        self.textEditMeaning.setText(new_value)

        self.setWindowTitle("Boost - {}*".format(self.repository.path))

    @pyqtSlot()
    def onEditItemClicked(self):
        current_row = self.listWidgetExpressions.currentRow()
        key = self.listWidgetExpressions.item(current_row).text()
        value = self.repository[key]

        self.dialogItemEdit.setExpression(key)
        self.dialogItemEdit.setMeaning(value)

        self.dialogItemEdit.pushButtonOk.setText("Изменить")
        self.dialogItemEdit.show()

    @pyqtSlot()
    def onDeleteItemClicked(self):
        row = self.listWidgetExpressions.currentRow()
        if -1 == row:
            return

        key = self.listWidgetExpressions.currentItem().text()
        if not key:
            return

        del self.repository[key]

        self.listWidgetExpressions.clear()

        expressions = self.repository.keys()
        if expressions:
            self.listWidgetExpressions.addItems(self.repository.keys())

            previous_row = row - 1 if row > 0 else 0
            self.listWidgetExpressions.setCurrentRow(previous_row)

        else:
            self.textEditMeaning.clear()

        self.setWindowTitle("Boost - {}*".format(self.repository.path))

    @pyqtSlot()
    def onActionNewTriggered(self):
        if self.repository.backup_path:
            message_box = QMessageBox(parent=self)
            message_box.setIcon(QMessageBox.Question)
            message_box.setWindowTitle("Внимание!")
            message_box.setText(
                "Файл {} был изменен! Сохранить изменения?".format(
                    self.repository.path
                )
            )

            ok_button = message_box.addButton("Ok", QMessageBox.ActionRole)
            cancel_button = message_box.addButton("Отмена", QMessageBox.ActionRole)

            message_box.exec()
            if message_box.clickedButton() == ok_button:
                self.saveRepository()
            else:
                self.restoreRepository()

        home_directory = Path(__file__).resolve().parents[2]
        default_path = home_directory / "dictionaries/new.db"
        self.repository = Repository(path=str(default_path))

        self.listWidgetExpressions.clear()
        self.textEditMeaning.clear()
        self.setWindowTitle("Boost - {}*".format(self.repository.path))

    @pyqtSlot()
    def onSaveActionTriggered(self):
        self.saveRepository()
        self.saveSettings()

        self.setWindowTitle("Boost - {}".format(self.repository.path))

    @pyqtSlot()
    def onSaveAsActionTriggered(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить как...", "", "*.db")

        if not path:
            return

        if not str(path).endswith(".db"):
            path += ".db"

        self.saveRepository(path=path)
        self.saveSettings()

        self.setWindowTitle("Boost - {}".format(self.repository.path))

    @pyqtSlot()
    def onActionOpenTriggered(self):
        if self.repository.backup_path:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Question)
            message_box.setWindowTitle("Внимание!")
            message_box.setText(
                "Файл {} был изменен! Сохранить изменения?".format(
                    self.repository.path
                )
            )

            ok_button = message_box.addButton("Ok", QMessageBox.ActionRole)
            cancel_button = message_box.addButton("Отмена", QMessageBox.ActionRole)

            message_box.exec()
            if message_box.clickedButton() == ok_button:
                self.saveRepository()

        path, _ = QFileDialog.getOpenFileName(self, "Открыть...", "", "*.db")
        if path:
            self.loadRepository(path=path)

    def closeEvent(self, event):
        path = self.repository.path
        if len(path) > 60:
            parts = Path(self.repository.path).parts
            parts_count = len(parts)
            if parts_count > 2:
                offset = 2
            elif parts_count > 3:
                offset = 3
            else:
                offset = 4

            path = ".../" + "/".join(Path(self.repository.path).parts[-offset:])

        if self.repository.backup_path:
            message_box = QMessageBox(parent=self)
            message_box.setIcon(QMessageBox.Question)
            message_box.setWindowTitle("Внимание!")
            message_box.setText(f"Файл <b>{path}</b> был изменен! Сохранить изменения?")

            ok_button = message_box.addButton("Ok", QMessageBox.ActionRole)
            cancel_button = message_box.addButton("Отмена", QMessageBox.ActionRole)

            message_box.exec_()
            if message_box.clickedButton() == ok_button:
                self.saveRepository()

        self.saveSettings()

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonDblClick:
            x = event.pos().x()
            y = event.pos().y()

            item_clicked = self.listWidgetExpressions.itemAt(x, y)
            if item_clicked:
                return QMainWindow.eventFilter(self, object, event)

            self.dialogItemAdd.show()

            return True

        return QMainWindow.eventFilter(self, object, event)

    def loadRepository(self, path: str):
        if not Path(path).is_file():
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Critical)
            message_box.setWindowTitle("Ошибка!")
            message_box.setText("Файл {} не найден!".format(path))
            message_box.setStandardButtons(QMessageBox.Ok)
            ok_button = message_box.button(QMessageBox.Ok)
            ok_button.setText("Ok")
            message_box.exec()

            return

        self.repository = Repository(path=path)

        self.setWindowTitle("Boost - {}".format(path))
        self.listWidgetExpressions.clear()
        self.textEditMeaning.clear()

        self.listWidgetExpressions.clear()
        self.textEditMeaning.clear()

        for key in self.repository.keys():
            self.listWidgetExpressions.addItem(key)

        self.listWidgetExpressions.setCurrentRow(0)

    def saveRepository(self, path: Optional[str] = None):
        self.repository.save(path=path)

    def restoreRepository(self):
        self.repository.restore()

    def createDefaultRepository(self, path: str):
        default_repository = Repository(path=path)
        default_repository["hello"] = "used to greet someone"

    def loadSettings(self):
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

            self.createDefaultRepository(path=str(default_path))
            self.loadRepository(path=str(default_path))

        elif not Path(repository_path).is_file():
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Critical)
            message_box.setWindowTitle("Ошибка")
            message_box.setText("Файл {} не найден!".format(repository_path))
            message_box.setStandardButtons(QMessageBox.Ok)
            ok_button = message_box.button(QMessageBox.Ok)
            ok_button.setText("Ok")
            message_box.exec()

            home_directory = Path(__file__).resolve().parents[2]
            default_path = home_directory / "dictionaries/hello.db"

            self.createDefaultRepository(path=str(default_path))
            self.loadRepository(path=str(default_path))

        else:
            self.loadRepository(path=str(repository_path))

    def saveSettings(self):
        settings = QSettings("RocketLabs", "Boost")
        settings.setValue("comboBoxHint_currentIndex", self.comboBoxHint.currentIndex())
        settings.setValue(
            "comboboxShuffle_currentIndex", self.comboBoxShuffle.currentIndex()
        )
        settings.setValue(
            "comboboxOrder_currentIndex", self.comboBoxOrder.currentIndex()
        )
        settings.setValue("repositoryPath", str(self.repository.path))
