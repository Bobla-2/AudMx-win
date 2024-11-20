import sys
from PySide6.QtWidgets import QLabel, QPushButton, QComboBox, QDialog, QGridLayout
from PySide6.QtCore import QSettings
from PySide6.QtGui import QFont
from typing import Callable, Dict, Any
from Bobla_lib.single_ton_meta import Singleton
import win32con
from win32api import keybd_event
import gc
class MenuSettingsButtonModule(metaclass=Singleton):
    def __init__(self, settings_tray: str, app_name: str, func: Callable[[Dict[str, Any]], Any]):
        self.cl = func
        self.__settings_tray: str = settings_tray
        self.__app_name: str = app_name
        self.dialog = QDialog()
        # self.dialog.setStyleSheet(style)
        font = QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(int(12))
        self.dialog.setFont(font)
        list_items = ["PLAY", "NEXT", "PREV", "MUTE"]

        self._set_BT_1 = QComboBox()
        self._set_BT_1.setFont(font)
        self._set_BT_1.addItems(list_items)
        self._set_BT_1_lb = QLabel("Низ")
        self._set_BT_1_lb.setObjectName("grei")
        self._set_BT_1_lb.setFont(font)
        self._set_BT_2 = QComboBox()
        self._set_BT_2.setFont(font)
        self._set_BT_2.addItems(list_items)
        self._set_BT_2_lb = QLabel("Середина")
        self._set_BT_2_lb.setObjectName("grei")
        self._set_BT_2_lb.setFont(font)
        self._set_BT_3 = QComboBox()
        self._set_BT_3.setFont(font)
        self._set_BT_3.addItems(list_items)
        self._set_BT_3_lb = QLabel("Верх")
        self._set_BT_3_lb.setObjectName("grei")
        self._set_BT_3_lb.setFont(font)

        self.__button = QPushButton("Сохранить")
        self.__button.clicked.connect(self.__safeSettingsApp)
        self.__button.setFont(font)
        self.__text = QLabel("Функции кнопок")
        self.__text.setFont(font)

        self.__layout = QGridLayout()
        self.__layout.addWidget(self.__text, 0, 0, 1, 1)
        self.__layout.addWidget(self._set_BT_1, 3, 1, 1, 1)
        self.__layout.addWidget(self._set_BT_1_lb, 3, 0, 1, 1)
        self.__layout.addWidget(self._set_BT_2, 2, 1, 1, 1)
        self.__layout.addWidget(self._set_BT_2_lb, 2, 0, 1, 1)
        self.__layout.addWidget(self._set_BT_3, 1, 1, 1, 1)
        self.__layout.addWidget(self._set_BT_3_lb, 1, 0, 1, 1)
        self.__layout.addWidget(self.__button, 5, 0, 1, 2)
        self.dialog.setLayout(self.__layout)

        self._set_BT_1.setCurrentText(QSettings().value(f"{self.__settings_tray}/BT1", False, type=str))
        self._set_BT_2.setCurrentText(QSettings().value(f"{self.__settings_tray}/BT2", False, type=str))
        self._set_BT_3.setCurrentText(QSettings().value(f"{self.__settings_tray}/BT3", False, type=str))

        self.dialog.show()
        self.dialog.closeEvent = self.on_close

    def on_close(self, _=None):
        if not _:
            self.dialog.close()
            return
        self.__class__._remove_instance()
        self.dialog.deleteLater()
        # referrers = gc.get_referrers(self)
        # print("1", referrers)
        del self
        # gc.collect()

    def __safeSettingsApp(self):
        settings = QSettings()
        settings.setValue(f"{self.__settings_tray}/BT1", self._set_BT_1.currentText())
        settings.setValue(f"{self.__settings_tray}/BT2", self._set_BT_2.currentText())
        settings.setValue(f"{self.__settings_tray}/BT3", self._set_BT_3.currentText())
        settings.sync()
        tmp = {"BT": [getattr(self, f"_set_BT_{i}").currentText() for i in range(1, 4)]}
        self.cl(tmp)
        self.on_close()
        del self

    @staticmethod
    def readBTMode(_settings_tray) -> dict:
        return {"BT": [QSettings().value(f"{_settings_tray}/BT{i}") for i in range(1, 4)]}

class ButtonModuleFunc():
    def __init__(self):
        self.list_func_BT = [ButtonModuleFunc.NEXT, ButtonModuleFunc.PLAY, ButtonModuleFunc.PREV]
        self.__mapping = {
            "NEXT": ButtonModuleFunc.NEXT,
            "PLAY": ButtonModuleFunc.PLAY,
            "PREV": ButtonModuleFunc.PREV,
            "MUTE": ButtonModuleFunc.MUTE
        }

    def setFunc(self, set: list) -> None:
        for num, st in enumerate(set):
            if st in self.__mapping:
                self.list_func_BT[num] = self.__mapping[st]

    def hanglerBT(self, comand: str) -> None:
        """
        #обработчик команд из сериал порта и иниирующий нажатия кнопок плеера
        :param comand: строка с командой типа ''
        :return: NONE
        """
        comand = str(comand).split("|")
        if (comand[1] == "pressed"):
            self.list_func_BT[int(comand[2][0])]()

    @staticmethod
    def PLAY():
        # win32con.VK_VOLUME_MUTE
        keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, 0, 0)
        keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def MUTE():
        # win32con.VK_VOLUME_MUTE
        keybd_event(win32con.VK_VOLUME_MUTE, 0, 0, 0)
        keybd_event(win32con.VK_VOLUME_MUTE, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def NEXT():
        keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, 0, 0)
        keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def PREV():
        keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, 0, 0)
        keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, win32con.KEYEVENTF_KEYUP, 0)

