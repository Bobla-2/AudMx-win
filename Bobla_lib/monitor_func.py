from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from Bobla_lib.single_ton_meta import Singleton

from typing import List
class Monitor(metaclass=Singleton):
    __abj = []
    __dict_monitor = {}
    __list_items = []
    __list_window = []

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
    def __init__(self):
        '''
        :param obj_adr:
        :param items: List[Tuple[QWidget, x size, y size]]
        :return: None
        '''
        self.__dict_monitor = self.getDictMonitor()

    def appendWindow(self,  obj_adr: QMainWindow, items: List[QWidget]) -> None:
        self.__abj = obj_adr
        self.__list_items = [(item, item.width(), item.height(), item.pos().x(), item.pos().y()) for item in items]
        self.__abj.windowHandle().screenChanged.connect(lambda screen: self.__editSize(screen.name()))
        self.__list_window.append((self.__abj, self.__list_items))
        self.__editSize(self.__abj.windowHandle().screen().name())
        self.__abj.show()

    def removeWindow(self, window):
        for num in range(len(self.__list_window)):
            if self.__list_window[num][0] == window:
                del self.__list_window[num]
                break

    def __editSize(self, screen_name: str) -> None:
        return
        self.__font = QtGui.QFont()
        self.__font.setFamily("Yu Gothic UI Semibold")
        self.__font.setPointSize(12)
        for wn in self.__list_window:
            skale = self.__dict_monitor[wn[0].windowHandle().screen().name()]
            print(skale)

            for obj, x, y, mx, my in wn[1]:
                obj.setFixedHeight(int(skale * y))
                obj.setFixedWidth(int(skale * x))
                if obj.__class__ != QMainWindow:
                    obj.move(int(skale * mx), int(skale * my))
                obj.setFont(self.__font)