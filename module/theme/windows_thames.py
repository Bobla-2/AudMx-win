import winreg
import sys
import os
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'

class ThemesWindows():

    @staticmethod
    def getStyle():

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
                print('тема:' + str(value))
    @staticmethod
    def getCSSFile(theme: int, path_to_W: str, path_to_B: str) -> str:

        if theme == 0:
            bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            path = os.path.join(bundle_dir, path_to_B)

            with open(path, "r+") as style_file:
                cssStyle = str(style_file.read())
                return cssStyle
        else:
            bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            path = os.path.join(bundle_dir, path_to_W)

            with open(path, "r+") as style_file:
                return str(style_file.read())
        return ""

    @staticmethod
    def getIconFile(theme: int, path_to_W: str, path_to_B: str) -> str:
        if theme == 0:
            bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            path = os.path.join(bundle_dir, path_to_B)
            return QIcon(path)
        else:
            bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            path = os.path.join(bundle_dir, path_to_W)
            return QIcon(path)
        return None

class AutoUpdateStile():
    __callback = []
    __old_theme = 0
    __set_fix_theme = "system"
    def __init__(self, interval=3000):
        '''
        :param callback: metod update style
        :param interval:
        '''
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__upDateStyle)
        self.__timer.setInterval(3000)
        self.__old_theme = ThemesWindows.getStyle()
        self.__timer.start()

    def appendedCallback(self, callback, path_to_W: str, path_to_B: str, type):
        self.__callback.append((callback, path_to_W, path_to_B, type))
        self.__setStyle(self.__old_theme)

    def __setStyle(self, old_theme):
        for cb in self.__callback:
            if cb[3] == "CSS":
                cb[0](ThemesWindows.getCSSFile(old_theme, cb[1], cb[2]))
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
        for cb in self.__callback:
            if cb[0] == callback:
                del cb
