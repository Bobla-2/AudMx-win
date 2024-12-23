import sys
from PySide6.QtWidgets import QLabel, QPushButton, QComboBox, QDialog, QGridLayout
from PySide6.QtCore import QSettings
from PySide6.QtGui import QFont
from typing import Callable, Dict, Any
from Bobla_lib.single_ton_meta import Singleton
from Bobla_lib.setting_menu_button import MenuSettingsButtonModule
from module.bobla_widgets.button import CheckButton
import gc
from module.UI_manager.theme.windows_thames import AutoUpdateStile

class MenuSettings(metaclass=Singleton):
    def __init__(self, set_tray: str, app_name: str, func: Callable[[Dict[str, Any]], Any]):
        self.cl = func
        self.__set_tray: str = set_tray
        self.__app_name: str = app_name
        # self.stl = style
        self.dialog = QDialog()
        # self.dialog.setStyleSheet(style)
        font = QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(int(12))
        self.dialog.setFont(font)

        self.__check_box_1 = CheckButton()
        self.__check_box_1.setFont(font)
        self.__check_box_1_lb = QLabel("Авто старт")
        self.__check_box_1_lb.setObjectName("grei")
        self.__check_box_1_lb.setFont(font)
        self.__check_box_3 = CheckButton()
        self.__check_box_3.setFont(font)
        self.__check_box_3_lb = QLabel("Авто serial")
        self.__check_box_3_lb.setFont(font)
        self.__check_box_3_lb.setObjectName("grei")
        self.__check_box_2 = CheckButton()
        self.__check_box_2.setFont(font)
        self.__check_box_2_lb = QLabel("Уведомления")
        self.__check_box_2_lb.setFont(font)
        self.__check_box_2_lb.setObjectName("grei")
        self.__set_theme_1 = QComboBox()
        self.__set_theme_1.setFont(font)
        self.__set_theme_1.addItems(["системная", "светлая", "темная"])
        self.__set_theme_1_lb = QLabel("тема")
        self.__set_theme_1_lb.setObjectName("grei")
        self.__set_theme_1_lb.setFont(font)
        self.__bt_set_bt = QPushButton("Функции кнопок")
        self.__bt_set_bt.clicked.connect(self.openButtonMenu)
        self.__bt_set_bt.setFont(font)
        self.__button = QPushButton("Сохранить")
        self.__button.clicked.connect(self.__safeSettingsApp)
        self.__button.setFont(font)
        self.__text = QLabel("<a href=\"https://github.com/Bobla-2/AudMx-win/releases/latest\">GitHub</a>")
        self.__text.setFont(font)
        self.__text.setOpenExternalLinks(True)

        self.__layout = QGridLayout()
        self.__layout.addWidget(self.__text, 0, 0, 1, 1)
        self.__layout.addWidget(self.__check_box_1.widget, 1, 1, 1, 1)
        self.__layout.addWidget(self.__check_box_1_lb, 1, 0, 1, 1)
        self.__layout.addWidget(self.__check_box_2.widget, 2, 1, 1, 1)
        self.__layout.addWidget(self.__check_box_2_lb, 2, 0, 1, 1)
        self.__layout.addWidget(self.__set_theme_1, 4, 1, 1, 1)
        self.__layout.addWidget(self.__set_theme_1_lb, 4, 0, 1, 1)
        self.__layout.addWidget(self.__bt_set_bt, 5, 0, 1, 1)
        self.__layout.addWidget(self.__button, 6, 0, 1, 2)
        self.dialog.setLayout(self.__layout)

        self.__set_theme_1.setCurrentText(QSettings().value(f"{self.__set_tray}/theme", False, type=str))
        self.__check_box_2.setChecked(QSettings().value(f"{self.__set_tray}/warning", False, type=int))
        self.__check_box_3.setChecked(QSettings().value(f"{self.__set_tray}/auto_ser_con", False, type=int))
        self.__check_box_1.setChecked(AvtoRunStatic.readAppToAvtoRun(self.__app_name))

        self.dialog.show()
        self.dialog.closeEvent = self.on_close
    def openButtonMenu(self):
        self._button_menu = MenuSettingsButtonModule(self.__set_tray, self.__app_name, self.cl)
        self.avto_udate_theme = AutoUpdateStile()
        self.avto_udate_theme.appendedCallback(self._button_menu.dialog.setStyleSheet, ":/qss/W_sylete",
                                               ":/qss/B_sylete", "CSS")
        self.avto_udate_theme.removeCallback(self._button_menu.dialog.setStyleSheet)


    @property
    def items(self):
        return ()
    def on_close(self, _=None):
        if not _:
            self.dialog.close()
            return
        if hasattr(self, "_button_menu"):
            del self._button_menu
        self.__class__._remove_instance()
        # referrers = gc.get_referrers(self.__check_box_1)
        # print("1", referrers)
        self.dialog.deleteLater()
        del self
        gc.collect()

    def __safeSettingsApp(self):
        settings = QSettings()
        settings.setValue(f"{self.__set_tray}/theme", self.__set_theme_1.currentText())
        # print(self.__check_box_2.isChecked())
        settings.setValue(f"{self.__set_tray}/warning", int(self.__check_box_2.isChecked()))
        settings.setValue(f"{self.__set_tray}/auto_ser_con", int(self.__check_box_3.isChecked()))
        settings.sync()
        if (self.__check_box_1.isChecked() == 0):
            AvtoRunStatic.removeAppToAvtoRun(self.__app_name)
        else:
            AvtoRunStatic.addAppToAvtoRun(self.__app_name, sys.argv[0])
        tmp = {}
        tmp["warning"] = self.__check_box_2.isChecked()
        if self.__set_theme_1.currentText() == "темная":
            tmp["theme"] = "black"
        elif self.__set_theme_1.currentText() == "светлая":
            tmp["theme"] = "white"
        else:
            tmp["theme"] = "system"
        self.cl(tmp)
        self.on_close()
        del self

    @staticmethod
    def readThemeMode(__set_tray: str) -> str:
        tm = QSettings().value(__set_tray + "/theme", False, type=str)
        if tm == "темная":
            return "black"
        elif tm == "светлая":
            return "white"
        else:
            return "system"

    @staticmethod
    def readVarningMode(__set_tray) -> str:
        return QSettings().value(f"{__set_tray}/warning", False, type=int)

    @staticmethod
    def readAutoSerialMode(__set_tray) -> str:
        return QSettings().value(f"{__set_tray}/auto_ser_con", False, type=int)


class AvtoRunStatic():
    __RUN_PATH = "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"

    @staticmethod
    def addAppToAvtoRun(name_app: str, path_to_app: str):
        settings = QSettings(AvtoRunStatic.__RUN_PATH, QSettings.NativeFormat)
        settings.setValue(name_app, path_to_app)

    @staticmethod
    def removeAppToAvtoRun(name_app: str):
        settings = QSettings(AvtoRunStatic.__RUN_PATH, QSettings.NativeFormat)
        settings.remove(name_app)

    @staticmethod
    def readAppToAvtoRun(name_app: str) -> bool:
        settings = QSettings(AvtoRunStatic.__RUN_PATH, QSettings.NativeFormat)
        return settings.contains(name_app)