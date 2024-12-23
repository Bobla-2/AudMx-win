import sys
from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox, QDialog, QGridLayout, QWidget, QStyledItemDelegate
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import Qt

from typing import Callable, Dict, Any

from module.other.single_ton_meta import Singleton
from module.UI_manager.monitor_func import Monitor
from module.bobla_widgets.button import CheckButton
from module.UI.warming_massage import WarmingMassage

# from updater.check import Updater
import subprocess
import os
import configparser

simple_settings_list = (
    ("/speed_test", bool, "укор. тест"),
    ("/auto_ser_con", bool, "Serial авто"),
    ("/warning", bool, "Уведомления"),
    ("/scale08", bool, "Реж. 10 inh"),
    ("/period_test", bool, "Период. Тест")
)

class MenuSettingsController(metaclass=Singleton):
    def __init__(self, set_path: str, app_name: str, func: Callable[[Dict[str, Any]], Any], mode: str, touch_mode=False):
        self.__touch_mode = touch_mode
        self.__mode = mode
        self.cl = func
        self.__set_path = set_path
        self.__app_name = app_name
        self.view = MenuSettingsView(touch_mode=True)
        self.model = MenuSettingsModel(self.__set_path, self.__mode)
        self.view.button_update.clicked.connect(self.__startUpdate)
        self.view.button.clicked.connect(self.__safeSettingsApp)
        theme_dict = {"black": "темная", "white": "светлая",  "system": "системная", "False": "системная"}
        print(self.model.getValue("/speed_test", bool))
        self.view.set_theme_1.setCurrentText(theme_dict[str(self.model.getValue("/theme", str))])
        self.view.check_box_as.setChecked(AvtoRunStatic.readAppToAvtoRun(self.__app_name))

        for ite in self.view.check_box_list:
            ite[1].setChecked(self.model.getValue(ite[2], bool))

        self.view.dialog.closeEvent = self.on_close
        self.ui_manager = Monitor()
        self.ui_manager.appendWindow(self.view.dialog, self.view.items)

    def __startUpdate(self):
        path = (os.path.abspath(__file__).replace("_internal\\Bobla_lib\\setting_menu.pyc", "") +
                "updater.exe")
        if os.path.isfile(path):
            subprocess.Popen([path])
            sys.exit()
        else:
            self.windowWar = WarmingMassage("Ошибка обновления:\nupdater.exe не найден")
            self.windowWar.setLinkOnWindows(self.windowWar)

    @property
    def items(self):
        return self.view.items

    def on_close(self, _=None):
        if not _:
            self.view.dialog.close()
            return
        self.view.dialog.deleteLater()
        self.ui_manager.removeWindow(self.view.dialog)
        self.__class__._remove_instance()
        self.view.dialog.deleteLater()
        del self

    def __safeSettingsApp(self):
        tmp = {}
        theme_dict = {"темная": "black", "светлая": "white", "системная": "system"}
        if self.model.getValue("/theme", str) != theme_dict[str(self.view.set_theme_1.currentText())]:
            self.model.setValue("/theme", theme_dict[self.view.set_theme_1.currentText()])
            tmp["theme"] = theme_dict[self.view.set_theme_1.currentText()]

        for ite in self.view.check_box_list:
            value = int(ite[1].isChecked())
            if self.model.getValue(ite[2], int) != value:
                self.model.setValue(ite[2], value)
                tmp[ite[2]] = value

        if (self.view.check_box_as.isChecked() == 0):
            AvtoRunStatic.removeAppToAvtoRun(self.__app_name)
        else:
            AvtoRunStatic.addAppToAvtoRun(self.__app_name, sys.argv[0])

        self.cl(tmp)
        self.on_close()
        del self


class MenuSettingsView:
    def __init__(self, parent=None, touch_mode=False):
        self.__touch_mode = touch_mode
        self.dialog = QDialog()
        # self.dialog.setBaseSize(1, 1)
        self.__layout = QGridLayout()
        self.__layout.setAlignment(Qt.AlignCenter)
        self.check_box_list = []
        global simple_settings_list
        for num, dt in enumerate(simple_settings_list):
            self.check_box_list.append((QLabel(dt[2]), CheckButton(), dt[0]))
            self.check_box_list[-1][0].setObjectName("grei")
            self.__layout.addWidget(self.check_box_list[-1][1].widget, num + 2, 1, 1, 1)
            self.__layout.addWidget(self.check_box_list[-1][0], num + 2, 0, 1, 1)
            if not self.__touch_mode:
                self.check_box_list[-1][0].setFixedSize(150, 30)
                self.check_box_list[-1][1].setFixedSize(30, 30)
            else:
                self.check_box_list[-1][0].setFixedSize(250, 60)
                self.check_box_list[-1][1].setFixedSize(50, 50)
        self.check_box_as = CheckButton()
        self.__check_box_as_lb = QLabel("Автозапуск прог.")
        self.__check_box_as_lb.setObjectName("grei")

        self.set_theme_1 = QComboBox()
        self.set_theme_1.addItems(["системная", "светлая", "темная"])
        self.__set_theme_1_lb = QLabel("тема")
        self.__set_theme_1_lb.setObjectName("grei")

        self.set_mod_test = QComboBox()
        self.set_mod_test.addItems(["сокр", "полн", "период"])
        self.__set_mod_test_lb = QLabel("тема")
        self.__set_mod_test_lb.setObjectName("grei")

        self.button_update = QPushButton("Обновить")
        self.button = QPushButton("Сохранить")
        if not self.__touch_mode:
            self.__check_box_as_lb.setFixedSize(150, 30)
            self.set_theme_1.setFixedSize(105, 30)
            self.button_update.setFixedSize(140, 30)
            self.check_box_as.setFixedSize(30, 30)
            self.button.setFixedSize(140, 30)
        else:
            self.__check_box_as_lb.setFixedSize(250, 60)
            self.set_theme_1.setFixedSize(130, 60)
            self.button_update.setFixedSize(250, 60)
            self.check_box_as.setFixedSize(50, 50)
            self.button.setFixedSize(250, 60)
            # self.set_theme_1.view().setMinimumHeight(100)
            # self.set_theme_1.view().setMinimumWidth(100)
            # delegate = QStyledItemDelegate(self.set_theme_1)
            # delegate.setItemSizeHint(100, 50)
            # self.set_theme_1.setItemDelegate(delegate)
        self.__layout.addWidget(self.button_update, 0, 0, 1, 2)
        self.__layout.addWidget(self.check_box_as.widget, 1, 1, 1, 1)
        self.__layout.addWidget(self.__check_box_as_lb, 1, 0, 1, 1)
        self.__layout.addWidget(self.set_theme_1, 15, 1, 1, 1)
        self.__layout.addWidget(self.__set_theme_1_lb, 15, 0, 1, 1)
        self.__layout.addWidget(self.button, 16, 0, 1, 2)
        self.dialog.setLayout(self.__layout)

        self.dialog.show()
        self.dialog.setFixedSize(self.dialog.size())

    @property
    def items(self):
        return ([item for item in list(self.__dict__.values()) if
                 issubclass(type(item), QWidget) and not issubclass(type(item), QDialog)] +
                [item for line in self.check_box_list for item in line if issubclass(type(item), QWidget)])


class MenuSettingsModel(metaclass=Singleton):
    def __init__(self, app_path: str, mode="ini"):
        self.__app_path = app_path
        self.__mode = mode
        self.__theme_dict = {"темная": "black", "светлая": "white", "системная": "system", "false": "system"}
        if self.__mode == "ini":
            self.__app_path = "./settings.ini"  # Путь к INI файлу
            print(self.__app_path)
            self.__config = configparser.ConfigParser()
            self.__config.read(self.__app_path)
        else:
            pass

    def __del__(self):
        self.__class__._remove_instance()

    def getValue(self, path: str, type_: type) -> Any:

        if self.__mode == "reg":
            if path == "/theme":
                return str(QSettings().value(self.__app_path + path, False))
            else:
                return type_(QSettings().value(self.__app_path + path, False))
        else:
            if path == "/theme":
                return str(self.__config.get("DEFAULT", path, fallback=False))
            else:
                return type_(int(self.__config.get("DEFAULT", path, fallback=False, raw=True)))


    def setValue(self, path: str, data: Any):
        if self.__mode == "reg":
            if path == "/theme":
                QSettings().setValue(self.__app_path + path, data)
            else:
                QSettings().setValue(self.__app_path + path, data)
        else:
            if path == "/theme":
                self.__config.set("DEFAULT", path, data)
            else:
                self.__config.set("DEFAULT", path, str(data))
            with open(self.__app_path, 'w') as configfile:
                self.__config.write(configfile)

    def setModeReg(self):
        self.__mode = "ini"
    def setModeIni(self):
        self.__mode = "reg"


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
