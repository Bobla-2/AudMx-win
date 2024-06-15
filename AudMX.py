from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
import sys
import win32con
import win32api
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer, QCoreApplication
from Bobla_lib.serialLib import SerCDC
from comtypes import CLSCTX_ALL
from Bobla_lib.icon_manager import IcomReader, VaveLight

from Bobla_lib.setting_menu import MenuSettings
from module.theme.windows_thames import AutoUpdateStile
from PySide6.QtGui import QCursor
from module.tray.trayApp import SystemTrayIcon
from module.ENUM.enums import LIGHT_MODE, dictVolumeDBtoProsent

ORGANIZATION_NAME = 'AudMX'
ORGANIZATION_DOMAIN = ''
APPLICATION_NAME = 'AudMX v1'
SETTINGS_TRAY = 'settings'

class MainClass(QWidget):
    volLevelApp = []
    __light_mode = -1

    last_process_list = []
    num_load_icon = -1
    teat_perer = 0
    open_process_list = []
    __comand_Buff = ''
    __count_presed_button = 0

    valve_light = None
    def __init__(self):
        super().__init__()

        self.trayIcon = SystemTrayIcon(self)
        self.trayIcon.show()
        self.trayIcon.flag_warning = MenuSettings.readVarningMode(SETTINGS_TRAY)
        self.trayIcon.SignalLIghtMode.connect(lambda mode: self.handleSignalLIghtMode(mode))
        self.cl_set = {}
        self.trayIcon.SignalActSet.connect(lambda: MenuSettings(SETTINGS_TRAY, APPLICATION_NAME, self.styleSheet(), self.setSettings))
        self.trayIcon.SignalButtonExit.connect(self.exitApp)

        self.ser = SerCDC(True)
        self.ser.setHanglerRead(self.hanglerReadSer)
        # self.audioSessions = AudioUtilities.GetAllSessions()

        self.timer_2 = QTimer()
        self.timer_2.timeout.connect(self.update_)
        self.timer_2.setInterval(5000)
        self.timer_2.start()
        self.update_()
        self.upDateListOpenProcces()
        self.icon_mass = []
        self.timer_setIconNum = QTimer()
        self.timer_setIconNum.timeout.connect(self.setIconNum)
        self.timer_setIconNum.setInterval(250)
        self.timer_is_work = QTimer()
        self.timer_is_work.timeout.connect(lambda: self.ser.writeSerial('ISWORK\n'))
        self.timer_is_work.setInterval(25000)
        self.timer_is_work.start()

        pid = 4097
        vid = 12346
        self.ser.SignalSerialStartOk.connect(self.startMassege)
        self.ser.autoConnect(vid, pid, 1000000, True)
        self.avto_udate_theme = AutoUpdateStile()
        self.avto_udate_theme.theme = MenuSettings.readThemeMode(SETTINGS_TRAY)
        self.avto_udate_theme.appendedCallback(self.setStyleSheet, "W_sylete", "B_sylete", "CSS")
        self.avto_udate_theme.appendedCallback(self.trayIcon.setIcon, "iconTrayW.png", "iconTrayB.png", "ICON")
        self.flag_setIconNum = 0
    def setSettings(self, set: dict):
        if 'warning' in set:
            self.trayIcon.flag_warning = set["warning"]
        if 'theme' in set:
            self.avto_udate_theme.theme = set["theme"]


    def hanglerReadSer(self, iner: str):
        if iner.find("BUTTON:") != -1:
            self.keyPleerHandle(iner)
        elif iner.find("|") != -1:
            if (iner != self.__comand_Buff):
                self.__comand_Buff = iner
                self.levelVolHandle(iner)
        elif iner.find("OK") != -1:
            if self.num_load_icon != -1:
                if self.flag_setIconNum == 1:
                    print("self.loadIconOnESP(1)--hanglerReadSer")
                    self.loadIconOnESP(1)
        elif iner.find("ERROR: -1") != -1:
            if self.flag_setIconNum == 1:
                if self.num_load_icon != -1:
                    print("self.loadIconOnESP(0)--hanglerReadSer")
                    self.loadIconOnESP(0)
        elif iner.find("Send 352 bytes") != -1:
            self.handleGetIcon()

    def upDateListOpenProcces(self):
        # a = AudioUtilities.GetAllSessions()
        self.open_process_list = [[session.Process.name(), session.Process.pid] for session in AudioUtilities.GetAllSessions() if session.Process] + [["master.exe", -1], ["system.exe", -1]]

    def update_(self):
        """
        #функция вызываеммая таймером и обновляющяя стиль приложения
        :return: None
        """
        if (self.ser.doesSerWork == 1):
            self.upDateListOpenProcces()
            if (self.last_process_list != self.open_process_list):
                IcomReader.setLastLevel(self.icon_mass, 0)
                self.volLevelApp = []
                self.last_process_list = self.open_process_list
                tempp = IcomReader.loadIcons(sys.argv[0][:sys.argv[0].rindex("\\")] + ".\\icon", self.open_process_list, 5)
                if ([i.name for i in tempp] != [i.name for i in self.icon_mass]):
                    self.icon_mass = tempp
                    self.ser.clearnQuwewe()
                    self.ser.clearnSend()
                    if self.__light_mode == LIGHT_MODE.VOLUME_LEVEL:
                        self.valve_light.updateList(self.icon_mass)
                    print("self.loadIconOnESP(1)--update_")
                    self.loadIconOnESP(1)

    def keyPleerHandle(self, comand: str) -> None:
        """
        #обработчик команд из сериал порта и иниирующий нажатия кнопок плеера
        :param comand: строка с командой типа ''
        :return: NONE
        """
        comand = str(comand).split("|")
        comand[1] = int(comand[1])
        if (comand[0] == "realised"):
            if (self.__count_presed_button > 0):
                self.__count_presed_button = 0
                return
            if comand[1] == 1:
                win32api.keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, 0, 0)
                win32api.keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, win32con.KEYEVENTF_KEYUP, 0)
            elif comand[1] == 0:
                win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, 0, 0)
                win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, win32con.KEYEVENTF_KEYUP, 0)
            elif comand[1] == 2:
                win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, 0, 0)
                win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, win32con.KEYEVENTF_KEYUP, 0)

        else:
            self.__count_presed_button += 1
            if (self.__count_presed_button > 10):
                if comand[1] == 1:
                    pass
                elif comand[1] == 0:
                    pass
                elif comand[1] == 2:
                    pass

    def levelVolHandle(self, comand: str) -> None:
        """
        #обработчик команд из сериал порта и выставляющий нужый уровень громкости
        :param comand: строка с командой типа ''
        :return: NONE
        """
        comand = str(comand).split("|")
        if (len(comand) != 5):
            return
        self.audioSessions = AudioUtilities.GetAllSessions()
        for i in range(5):
            if self.icon_mass[i].name == "":
                
                return
            self.icon_mass[i].volume_level = int(int(comand[i])/10.24)
            if self.icon_mass[i].last_volume_level != self.icon_mass[i].volume_level:
                self.icon_mass[i].last_volume_level = self.icon_mass[i].volume_level
                if self.icon_mass[i].name == "master.exe":
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = interface.QueryInterface(IAudioEndpointVolume)
                    volume.SetMasterVolumeLevel(dictVolumeDBtoProsent[self.icon_mass[i].volume_level], None)
                    continue
                for session in self.audioSessions:
                    if session.Process and session.Process.name() == self.icon_mass[i].name:
                        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                        volume.SetMasterVolume(float(self.icon_mass[i].volume_level) / 100, None)
                    elif (self.icon_mass[i].name == "system" and str(session)[
                        -5] == 'DisplayName: @%SystemRoot%\System32\AudioSrv.Dll'):
                        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                        volume.SetMasterVolume(float(self.icon_mass[i].volume_level) / 100, None)

    def handleSignalLIghtMode(self, mode: int):
        if mode == LIGHT_MODE.WHITE.value:
            self.__light_mode = LIGHT_MODE.WHITE
            self.ser.writeSerial("SET_LIGHT:white")
        if mode == LIGHT_MODE.WAVE.value:
            self.__light_mode = LIGHT_MODE.WAVE
            self.ser.writeSerial("SET_LIGHT:wave")
        if mode == LIGHT_MODE.VOLUME_LEVEL.value:
            self.__light_mode = LIGHT_MODE.VOLUME_LEVEL
            self.ser.writeSerial("SET_LIGHT:level_value")
            self.valve_light = VaveLight(self.icon_mass, self.ser.writeSerial)
            self.valve_light.avtoUpdateStart()
        else:
            if self.valve_light != None:
                self.valve_light.stop()

    def startMassege(self):
        """
        #вызываеться послесигнала о подключении и запускает перврначальную настройку(записывает картинки в микщер)
        :return:
        """
        self.last_process_list = []
        self.icon_mass.clear()
        self.num_load_icon = -1

    def loadIconOnESP(self, ans=0):
        print(self.num_load_icon)
        self.num_load_icon = self.num_load_icon + ans
        print(self.num_load_icon)
        if self.num_load_icon == -1:
            return
        if self.num_load_icon == 0:
            self.timer_setIconNum.start()

            if self.__light_mode == LIGHT_MODE.VOLUME_LEVEL:
                self.valve_light.avtoUpdateStop()
                print("avtoUpdateStop")
                return
        print(self.num_load_icon)
        if (self.num_load_icon == 5):
            self.num_load_icon = -1
            self.flag_setIconNum = 0
            if self.__light_mode == LIGHT_MODE.VOLUME_LEVEL:
                self.valve_light.avtoUpdateStart()
            return
        self.setIconNum()

    def setIconNum(self):
        self.ser.writeSerial("SET_ICON " + str(self.icon_mass[self.num_load_icon].num) + "\n")
        self.flag_setIconNum = 1
        self.timer_setIconNum.stop()

    def handleGetIcon(self):
        self.ser.writeByteSerial(self.icon_mass[self.num_load_icon].icon)

    def exitApp(self):
        if self.__light_mode == LIGHT_MODE.VOLUME_LEVEL:
            self.valve_light.stop()
        QCoreApplication.exit()

if __name__ == '__main__':
    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    app.setQuitOnLastWindowClosed(False)
    window = MainClass()
    sys.exit(app.exec())
