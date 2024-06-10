import sys
from PySide6.QtWidgets import QCheckBox, QLabel, QPushButton, QComboBox, QDialog, QGridLayout, QApplication
from PySide6.QtCore import QSettings
from PySide6.QtGui import QFont
from typing import Callable, Dict, Any
from threading import Lock, Thread
class Singleton(type):
  _instances = {}
  # _lock: Lock = Lock()
  def __call__(cls, *args, **kwargs):
      # with cls._lock:
      if cls not in cls._instances:
          instance = super().__call__(*args, **kwargs)
          cls._instances[cls] = instance
      return cls._instances[cls]

  def _remove_instance(cls):
      if cls in cls._instances:
          del cls._instances[cls]

class MenuSettings(metaclass=Singleton):
    __set_tray = ""
    __app_name = ""

    def __init__(self, set_tray: str, app_name: str, style: str, func: Callable[[Dict[str, Any]], Any],  parent=None):
        # super().__init__(parent)
        self.cl = func
        self.__set_tray = set_tray
        self.__app_name = app_name
        self.dialog = QDialog()
        self.dialog.setStyleSheet(style)
        font = QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(int(12))
        self.dialog.setFont(font)

        self.__check_box_1 = QCheckBox()
        self.__check_box_1.setFont(font)
        self.__check_box_1_lb = QLabel("Авто старт")
        self.__check_box_1_lb.setFont(font)
        self.__check_box_2 = QCheckBox()
        self.__check_box_2.setFont(font)
        self.__check_box_2_lb = QLabel("Уведомления")
        self.__check_box_2_lb.setFont(font)
        self.__set_theme_1 = QComboBox()
        self.__set_theme_1.setFont(font)
        self.__set_theme_1.addItems(["системная", "светлая", "темная"])
        self.__set_theme_1_lb = QLabel("тема")
        self.__set_theme_1_lb.setFont(font)
        self.__button = QPushButton("Сохранить")
        self.__button.clicked.connect(self.__safeSettingsApp)
        self.__button.setFont(font)

        self.__layout = QGridLayout()
        self.__layout.addWidget(self.__check_box_1, 1, 1, 1, 1)
        self.__layout.addWidget(self.__check_box_1_lb, 1, 0, 1, 1)
        self.__layout.addWidget(self.__check_box_2, 2, 1, 1, 1)
        self.__layout.addWidget(self.__check_box_2_lb, 2, 0, 1, 1)
        self.__layout.addWidget(self.__set_theme_1, 3, 1, 1, 1)
        self.__layout.addWidget(self.__set_theme_1_lb, 3, 0, 1, 1)
        self.__layout.addWidget(self.__button, 4, 0, 1, 2)
        self.dialog.setLayout(self.__layout)

        self.__set_theme_1.setCurrentText(QSettings().value(self.__set_tray + "/theme", False, type=str))
        self.__check_box_2.setChecked(QSettings().value(self.__set_tray + "/warning", False, type=int))
        self.__check_box_1.setChecked(AvtoRunStatic.readAppToAvtoRun(self.__app_name))
        self.dialog.show()
        self.dialog.closeEvent = self.on_close       # if self.dialog.exec_() == QDialog.DialogCode.Accepted:
        #     pass
        # self.dialog.deleteLater()
    def on_close(self, event):
        self.__class__._remove_instance()
        del self


    def __safeSettingsApp(self):
        settings = QSettings()
        settings.setValue(self.__set_tray + "/theme", self.__set_theme_1.currentText())
        print(self.__check_box_2.isChecked())
        settings.setValue(self.__set_tray + "/warning", int(self.__check_box_2.isChecked()))
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

    @staticmethod
    def readThemeMode(__set_tray) -> str:
        tm = QSettings().value(__set_tray + "/theme", False, type=str)
        if tm == "темная":
            return "black"
        elif tm == "светлая":
            return "white"
        else:
            return "system"

    @staticmethod
    def readVarningMode(__set_tray) -> str:
        return QSettings().value(__set_tray + "/warning", False, type=int)


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


class Monitor():
    @staticmethod
    def getDictMonitor() -> dict:
        app = QApplication.instance()  # Получаем экземпляр приложения
        if app is None:
            app = QApplication([])  # Создаем приложение, если его нет

        dict_monitor = {}

        for screen in app.screens():
            dpi = screen.logicalDotsPerInch()
            scale_factor = dpi / 96.0
            dict_monitor[screen.name()] = scale_factor
        return dict_monitor
    # def temp(self, parent):
    #     parent.windowHandle().screenChanged.connect(lambda screen: parent.editSize(screen.name()))
    #
