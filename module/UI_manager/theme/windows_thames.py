import platform
from PySide6.QtCore import QTimer, QFile, QIODevice, QTextStream
from PySide6.QtGui import QIcon
from module.resurce import resources
reg = None
reg_path = None
system_name = platform.system()
try:
    if system_name == "Windows":
        import winreg
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
except:
    pass

class ThemesWindows:

    @staticmethod
    def getStyle():
        global system_name
        global reg
        global reg_path
        if system_name == "Windows":

            try:
                reg_key = winreg.OpenKey(reg, reg_path)
            except FileNotFoundError:
                pass

            for i in range(1024):
                try:
                    value_name, value, _ = winreg.EnumValue(reg_key, i)
                    if value_name == 'SystemUsesLightTheme':
                        return value
                except:
                    pass
        return 0
    @staticmethod
    def getCSSFile(theme: int, path_to_W: str, path_to_B: str) -> str:
        if theme == 0:
            stream = QFile(path_to_B)
            stream.open(QIODevice.ReadOnly)
            t = QTextStream(stream).readAll()
            return t
        else:
            stream = QFile(path_to_W)
            stream.open(QIODevice.ReadOnly)
            t = QTextStream(stream).readAll()
            return t
        return ""

    @staticmethod
    def getIconFile(theme: int, path_to_W: str, path_to_B: str) -> str:
        if theme == 0:
            return QIcon(path_to_B)
        else:
            return QIcon(path_to_W)
        return None

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class AutoUpdateStile():
    __callback = []
    __old_theme = -1
    __set_fix_theme = "system"
    def __init__(self, interval=3000):
        '''
        :param callback: metod update style
        :param interval:
        '''
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__upDateStyle)
        self.__timer.setInterval(6000)
        self.__old_theme = ThemesWindows.getStyle()
        self.__timer.start()

    def appendedCallback(self, callback, path_to_W: str, path_to_B: str, type):
        self.__callback.append((callback, path_to_W, path_to_B, type))
        self.__setStyle(self.__old_theme)


    def __setStyle(self, old_theme):
        for cb in self.__callback:
            if cb[3] == "CSS":
                h = ThemesWindows.getCSSFile(old_theme, cb[1], cb[2])
                cb[0](h)
            elif cb[3] == "ICON":
                cb[0](ThemesWindows.getIconFile(old_theme, cb[1], cb[2]))

    def __upDateStyle(self):
        if self.__changeThemes():
            self.__setStyle(self.__old_theme)

    def __changeThemes(self):
        if self.__old_theme != ThemesWindows.getStyle():
            self.__old_theme = not self.__old_theme
            return True
        return False

    @property
    def theme(self):
        return self.__set_fix_theme

    @theme.setter
    def theme(self, th):
        self.__set_fix_theme = th
        if self.__set_fix_theme != "system":
            if self.__set_fix_theme == "white":
                self.__old_theme = 1
                self.__setStyle(1)
            else:
                self.__old_theme = 0
                self.__setStyle(0)
            self.__timer.stop()
        else:
            self.__timer.start()
            self.__setStyle(self.__old_theme)

    def removeCallback(self, callback: object):
        for num in range(len(self.__callback)):
            if self.__callback[num][0] == callback:
                del self.__callback[num]
                break

