from module.UI_manager.theme.windows_thames import AutoUpdateStile
from module.UI_manager.monitor_func import Monitor

from PySide6 import QtWidgets

class WarmingMassage():
    def __init__(self, text: str) -> None:

        self.__msgBox = QtWidgets.QDialog()
        self.__msgBox.setWindowTitle("")
        self.__layout = QtWidgets.QGridLayout()
        self.__level_lb = QtWidgets.QLabel(text)
        self.__level_lb.setFixedSize(300, 100)
        self.__button = QtWidgets.QPushButton("ОК")
        self.__layout.addWidget(self.__level_lb, 1, 0, 1, 1)
        self.__layout.addWidget(self.__button, 3, 0, 1, 2)
        self.__button.clicked.connect(self.__close)
        self.__button.setFixedSize(300, 50)
        self.__msgBox.setLayout(self.__layout)
        self.__msgBox.show()
        self.avto_udate_theme = AutoUpdateStile()
        self.avto_udate_theme.appendedCallback(self.__msgBox.setStyleSheet, ":/qss/W_sylete", ":/qss/B_sylete",
                                               "CSS")
        self.__link = None
        self.timp = Monitor()
        self.timp.appendWindow(self.__msgBox, self.items)

    def setLinkOnWindows(self, link):
        self.__link = link

    def __close(self):
        self.avto_udate_theme.removeCallback(self.__msgBox.setStyleSheet)
        self.__msgBox.close()
        if self.__link:
            del self.__link
        del self

    @property
    def items(self):
        return [self.__button, self.__level_lb]
