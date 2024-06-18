from PySide6.QtWidgets import QApplication, QWidget
from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PySide6.QtCore import QObject
from typing import List, Tuple, Any
class Monitor():
    __abj = []
    __dict_monitor = {}
    __list_items = []

    def getDictMonitor(self) -> dict:
        app = QApplication.instance()  # Получаем экземпляр приложения
        if app is None:
            app = QApplication([])  # Создаем приложение, если его нет

        dict_monitor = {}

        for screen in app.screens():
            dpi = screen.logicalDotsPerInch()
            scale_factor = dpi / 96.0
            dict_monitor[screen.name()] = scale_factor
        self.__dict_monitor = dict_monitor
        return dict_monitor
    def setAutoSkale(self, obj_adr: QMainWindow, items: List[Tuple[QWidget, int, int]]) -> None:
        '''
        :param obj_adr:
        :param items: List[Tuple[QWidget, x size, y size]]
        :return: None
        '''
        self.__dict_monitor = self.getDictMonitor()
        self.__abj = obj_adr
        self.__list_items = items
        self.__abj.show()
        self.__abj.windowHandle().screenChanged.connect(lambda screen: self.__editSize(screen.name()))
        self.__font = QtGui.QFont()
        self.__font.setFamily("Yu Gothic UI Semibold")
        self.__font.setPointSize(12)
    def __editSize(self):
        for obj, x, y in self.__list_items:
            obj.setFixedSize(x, y)
            obj.setFont(self.__font)


