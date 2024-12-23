from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
import sys
import win32con
import win32api
# import tracemalloc

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer, QCoreApplication
from comtypes import CLSCTX_ALL
from Bobla_lib.icon_manager import IcomReader #, VaveLight
from Bobla_lib.setting_menu import MenuSettings
from Bobla_lib.serial_blu import ConectAudMX
from Bobla_lib.setting_menu_button import MenuSettingsButtonModule, ButtonModuleFunc
from module.UI_manager.theme.windows_thames import AutoUpdateStile
from module.UI.tray.trayApp import SystemTrayIcon
from module.ENUM.enums import dictVolumeDBtoProsent# LIGHT_MODE,

ORGANIZATION_NAME = 'AudMX'
ORGANIZATION_DOMAIN = ''
APPLICATION_NAME = 'AudMX v1.5'
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
        # tracemalloc.start()
        self.trayIcon = SystemTrayIcon(self)
        self.trayIcon.show()
        # self.trayIcon.menu_light.setStyleSheet("border-radius: 10px;")
        self.trayIcon.flag_warning = MenuSettings.readVarningMode(SETTINGS_TRAY)
        # self.trayIcon.SignalLIghtMode.connect(lambda mode: self.handleSignalLIghtMode(mode))

        self.cl_set = {}
        self.trayIcon.SignalActSet.connect(self.openMenuSettings)
        self.trayIcon.SignalButtonExit.connect(self.exitApp)
        self.timer_2 = QTimer()
        self.timer_2.timeout.connect(self.update_)
        self.timer_2.setInterval(5000)
        self.timer_2.start()
        self.icon_mass = []
        self.timer_setIconNum = QTimer()
        self.timer_setIconNum.timeout.connect(self.setIconNum)
        self.timer_setIconNum.setInterval(250)
        self.ser = ConectAudMX(True)
        # self.update_(True)
        self.upDateListOpenProcces()
        self.timer_is_work = QTimer()
        self.timer_is_work.timeout.connect(lambda: self.ser.writeSerial('ISWORK\n'))
        self.timer_is_work.setInterval(14000)
        self.timer_is_work.start()
        self.ser.setHanglerRead(self.hanglerReadSer)
        self.trayIcon.SignalChangeBluSer.connect(self.ser.changMod)

        pid = 4097
        vid = 12346
        self.ser.SignalSerialStartOk.connect(self.startMassege)
        self.ser.autoConnect(vid, pid, 1000000, True)
        self.avto_udate_theme = AutoUpdateStile()
        self.avto_udate_theme.theme = MenuSettings.readThemeMode(SETTINGS_TRAY)
        self.avto_udate_theme.appendedCallback(self.setStyleSheet, ":/qss/W_sylete", ":/qss/B_sylete", "CSS")
        self.avto_udate_theme.appendedCallback(self.trayIcon.setIcon, ":/icons/iconTrayW.png", ":/icons/iconTrayB.png", "ICON")
        self.flag_setIconNum = 0
        self.button_handler = ButtonModuleFunc()
        self.setSettings(MenuSettingsButtonModule.readBTMode(SETTINGS_TRAY))

    def setSettings(self, set: dict):

        if 'warning' in set:
            self.trayIcon.flag_warning = set["warning"]
        if 'theme' in set:
            self.avto_udate_theme.theme = set["theme"]
        if 'BT' in set:
            self.button_handler.setFunc(set["BT"])
            # del self.menu._button_menu
        else:
            del self.menu
    def openMenuSettings(self):
        self.menu = MenuSettings(SETTINGS_TRAY, APPLICATION_NAME, self.setSettings)
        self.avto_udate_theme = AutoUpdateStile()
        self.avto_udate_theme.appendedCallback(self.menu.dialog.setStyleSheet, ":/qss/W_sylete",
                                               ":/qss/B_sylete", "CSS")
        self.avto_udate_theme.removeCallback(self.menu.dialog.setStyleSheet)


    def hanglerReadSer(self, iner: str):
        # print("hanglerReadSer:  " + iner)
        if iner.find("BUTTON") != -1:
            self.button_handler.hanglerBT(iner)
        elif iner.find("|") != -1:
            if (iner != self.__comand_Buff):
                self.__comand_Buff = iner
                self.levelVolHandle(iner)
        elif iner.find("OK") != -1:
            if self.num_load_icon != -1:
                if self.flag_setIconNum == 1:
                    # print("self.loadIconOnESP(1)--hanglerReadSer")
                    self.loadIconOnESP(1)
        elif iner.find("ERROR: -1") != -1:
            if self.flag_setIconNum == 1:
                if self.num_load_icon != -1:
                    # print("self.loadIconOnESP(0)--hanglerReadSer")
                    self.loadIconOnESP(0)
        elif iner.find("Send 352 bytes") != -1:
            print("iner.find(Send 352 bytes)")
            self.handleGetIcon()
        elif iner.find("bluet") != -1:
            self.trayIcon.masegeWarningBLE()

    def upDateListOpenProcces(self):
        self.open_process_list = [[session.Process.name(), session.Process.pid] for session in AudioUtilities.GetAllSessions() if session.Process] + [["master.exe", -1], ["system.exe", -1]]

    def update_(self, tp=False):


        """
        #функция вызываеммая таймером и обновляющяя стиль приложения
        :return: None
        """
        # print(self.ser.doesSerWork)
        if (self.ser.doesSerWork == 1 or tp):
            self.upDateListOpenProcces()
            if (self.last_process_list != self.open_process_list):
                IcomReader.setLastLevel(self.icon_mass, 0)
                self.last_process_list = self.open_process_list
                tempp = IcomReader.loadIcons(sys.argv[0][:sys.argv[0].rindex("\\")] + ".\\icon", self.open_process_list, 5)
                if ((i.name for i in tempp) != (i.name for i in self.icon_mass)):
                    self.icon_mass = tempp
                    self.ser.clearnQuwewe()
                    self.ser.clearnSend()
                    # if self.__light_mode == LIGHT_MODE.VOLUME_LEVEL:
                    #     self.valve_light.updateList(self.icon_mass)
                    if (self.ser.doesSerWork == 1):
                        print("self.loadIconOnESP(1)--update_")
                        self.loadIconOnESP(1)



    def levelVolHandle(self, comand: str) -> None:
        # snapshot = tracemalloc.take_snapshot()
        # top_stats = snapshot.statistics('lineno')
        # for stat in top_stats[:80]:  # Показать топ-10 строк по потреблению памяти
        #     print(stat)
        """
        #обработчик команд из сериал порта и выставляющий нужый уровень громкости
        :param comand: строка с командой типа ''
        :return: NONE
        """
        if not self.icon_mass:
            return
        comand = comand.split("|")
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
                    elif (self.icon_mass[i].name == "system" and str(session)[-5] == 'DisplayName: @%SystemRoot%\System32\AudioSrv.Dll'):
                        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                        volume.SetMasterVolume(float(self.icon_mass[i].volume_level) / 100, None)

    # def handleSignalLIghtMode(self, mode: int):
    #     if mode == LIGHT_MODE.WHITE.value:
    #         self.__light_mode = LIGHT_MODE.WHITE
    #         self.ser.writeSerial("SET_LIGHT:white")
    #     if mode == LIGHT_MODE.WAVE.value:
    #         self.__light_mode = LIGHT_MODE.WAVE
    #         self.ser.writeSerial("SET_LIGHT:wave")
    #     if mode == LIGHT_MODE.VOLUME_LEVEL.value:
    #         self.__light_mode = LIGHT_MODE.VOLUME_LEVEL
    #         self.ser.writeSerial("SET_LIGHT:level_value")
    #         self.valve_light = VaveLight(self.icon_mass, self.ser.writeSerial)
    #         self.valve_light.avtoUpdateStart()
    #     else:
    #         if self.valve_light != None:
    #             self.valve_light.stop()

    def startMassege(self):
        """
        #вызываеться послесигнала о подключении и запускает перврначальную настройку(записывает картинки в микщер)
        :return:
        """
        print("startMassege")
        self.ser.writeSerial("ISWORK\n")
        self.last_process_list = []
        self.icon_mass.clear()
        # self.update_()
        self.num_load_icon = -1

    def loadIconOnESP(self, ans=0):
        print(self.num_load_icon)
        self.num_load_icon = self.num_load_icon + ans
        print(self.num_load_icon)
        if self.num_load_icon == -1:
            return
        if self.num_load_icon == 0:
            self.timer_setIconNum.start()

            # if self.__light_mode == LIGHT_MODE.VOLUME_LEVEL:
            #     self.valve_light.avtoUpdateStop()
            #     print("avtoUpdateStop")
            #     return
        print(self.num_load_icon)
        if (self.num_load_icon == 5):
            self.num_load_icon = -1
            self.flag_setIconNum = 0
            # if self.__light_mode == LIGHT_MODE.VOLUME_LEVEL:
            #     self.valve_light.avtoUpdateStart()
            return
        self.setIconNum()

    def setIconNum(self):
        self.ser.writeSerial("SET_ICON " + str(self.icon_mass[self.num_load_icon].num) + "\n")
        self.flag_setIconNum = 1
        self.timer_setIconNum.stop()

    def handleGetIcon(self):
        self.ser.writeByteSerial(self.icon_mass[self.num_load_icon].icon)

    def exitApp(self):
        # if self.__light_mode == LIGHT_MODE.VOLUME_LEVEL:
        #     self.valve_light.stop()
        QCoreApplication.exit()

if __name__ == '__main__':
    QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(ORGANIZATION_NAME)
    app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    app.setQuitOnLastWindowClosed(False)
    window = MainClass()
    sys.exit(app.exec())
