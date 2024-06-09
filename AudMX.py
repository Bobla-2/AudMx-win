from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
import sys
import win32con
import win32api
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QWidget
from PySide6.QtCore import QTimer, Signal, QCoreApplication, QPoint
from Bobla_lib.serialLib import SerCDC
from comtypes import CLSCTX_ALL
from Bobla_lib.icon_manager import IcomReader, VaveLight

from Bobla_lib.setting_menu import MenuSettings
from module.theme.windows_thames import AutoUpdateStile
from PySide6.QtGui import QCursor
from module.tray.trayApp import SystemTrayIcon
from module.ENUM.enums import LIGHT_MODE

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
    dictVolumeDBtoProsent = [-65.25,
                             -64.49741,
                             -58.173828125,
                             -50.437278747558594,
                             -47.282318115234375,
                             -46.02272033691406,
                             -42.34019088745117,
                             -40.06081008911133,
                             -38.07908630371094,
                             -36.32617950439453,
                             -34.75468063354492,
                             -33.33053970336914,
                             -32.02846908569336,
                             -30.829191207885742,
                             -29.7176513671875,
                             -28.681884765625,
                             -27.71221923828125,
                             -26.800716400146484,
                             -25.940793991088867,
                             -25.126928329467773,
                             -24.35443115234375,
                             -23.61930274963379,
                             -22.918092727661133,
                             -22.2478084564209,
                             -21.605838775634766,
                             -20.989887237548828,
                             -20.397926330566406,
                             -19.828153610229492,
                             -19.278972625732422,
                             -18.748943328857422,
                             -18.236774444580078,
                             -17.741300582885742,
                             -17.261470794677734,
                             -16.796323776245117,
                             -16.344989776611328,
                             -15.906672477722168,
                             -15.480639457702637,
                             -15.06622314453125,
                             -14.662806510925293,
                             -14.269820213317871,
                             -13.886737823486328,
                             -13.513073921203613,
                             -13.148375511169434,
                             -12.792222023010254,
                             -12.444223403930664,
                             -12.10401439666748,
                             -11.771252632141113,
                             -11.445619583129883,
                             -11.12681770324707,
                             -10.814563751220703,
                             -10.508596420288086,
                             -10.20866584777832,
                             -9.914539337158203,
                             -9.625996589660645,
                             -9.342827796936035,
                             -9.064839363098145,
                             -8.791844367980957,
                             -8.523664474487305,
                             -8.260135650634766,
                             -8.001096725463867,
                             -7.746397495269775,
                             -7.49589729309082,
                             -7.249458312988281,
                             -7.006951332092285,
                             -6.768252372741699,
                             -6.5332441329956055,
                             -6.301812648773193,
                             -6.073853492736816,
                             -5.849262237548828,
                             -5.627941608428955,
                             -5.409796714782715,
                             -5.194738864898682,
                             -4.982679843902588,
                             -4.7735395431518555,
                             -4.567237854003906,
                             -4.363698959350586,
                             -4.162849426269531,
                             -3.9646193981170654,
                             -3.7689411640167236,
                             -3.5757486820220947,
                             -3.384982109069824,
                             -3.196580171585083,
                             -3.0104846954345703,
                             -2.8266398906707764,
                             -2.6449923515319824,
                             -2.4654886722564697,
                             -2.288081407546997,
                             -1.7679541110992432,
                             -1.5984597206115723,
                             -1.4308334589004517,
                             -1.2650364637374878,
                             -1.101028561592102,
                             -0.9387713074684143,
                             -0.7782278060913086,
                             -0.6193622946739197,
                             -0.4621390104293823,
                             -0.3065262734889984,
                             -0.15249048173427582,
                             0.0,
                             0.0]
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
            self.icon_mass[i].volume_level = int(int(comand[i])/10.24)
            if self.icon_mass[i].name == "":
                return
            if self.icon_mass[i].last_volume_level != self.icon_mass[i].volume_level:
                self.icon_mass[i].last_volume_level = self.icon_mass[i].volume_level
                if self.icon_mass[i].name == "master.exe":
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume = interface.QueryInterface(IAudioEndpointVolume)
                    volume.SetMasterVolumeLevel(self.dictVolumeDBtoProsent[self.icon_mass[i].volume_level], None)
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
