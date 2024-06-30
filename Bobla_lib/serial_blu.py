from Bobla_lib.serialLib import SerCDC

from PySide6.QtCore import QIODevice, Signal, QObject, QTimer
from Bobla_lib.test_py_func import MyBlue
from enum import Enum


import asyncio


class Mod(Enum):
    BLU = 0
    SER = 1

class ConectAudMX(QObject):
    SignalSerialStartOk = Signal()
    __mod = Mod.SER
    __loop = None
    __data_to_connect = []

    def __init__(self, _):

        super(ConectAudMX, self).__init__()
        self.ser = SerCDC(True)
        self.blu = MyBlue(self.handleBluStartOk)
        # handler = BluetoothHandler()
        # asyncio.run(handler.main())
        # self.blu.SignalSerialStartOk.connect(lambda : print("2093847"))
        self.ser.SignalSerialStartOk.connect(self.SignalSerialStartOk.emit)
        # self.blu.SignalBluStartOk.connect(self.SignalSerialStartOk.emit)

    # Connect the signal to a slot

    # Define the slot method that handles the signal
    def handleBluStartOk(self):
        # pass
        self.SignalSerialStartOk.emit()
    def setHanglerRead(self, hangler):
        self.ser.setHanglerRead(hangler)
        self.blu.setHanglerRead(hangler)

    def clearnSend(self):
        self.ser.clearnSend()

    def clearnQuwewe(self):
        self.ser.clearnQuwewe()

    def changMod(self):
        if self.__mod == Mod.SER:
            self.__mod = Mod.BLU
            self.ser.closeSerial()
            self.autoConnect(self.__data_to_connect[0], self.__data_to_connect[1], self.__data_to_connect[2],
                             self.__data_to_connect[3])
        else:
            self.__mod = Mod.SER
            self.blu.close()
            self.autoConnect(self.__data_to_connect[0], self.__data_to_connect[1], self.__data_to_connect[2],
                             self.__data_to_connect[3])

    @property
    def doesSerWork(self):
        if self.__mod == Mod.SER:
            return self.ser.doesSerWork
        else:
            return self.blu.doesBluWork

    def autoConnect(self, vid, pid, buad_rate, reconnect):
        self.__data_to_connect = [vid, pid, buad_rate, reconnect]
        print("autoConnect")
        if self.__mod == Mod.SER:
            self.ser.autoConnect(vid, pid, buad_rate, reconnect)
        else:
            self.blu.autoConnect("AudMX")


    def writeSerial(self, str_):
        if self.__mod == Mod.SER:
            self.ser.writeSerial(str_)
        else:
            return
            self.blu.write(str_)

    def writeByteSerial(self, str_):
        if self.__mod == Mod.SER:
            self.ser.writeByteSerial(str_)
        else:
            return
            self.blu.write(str_)


