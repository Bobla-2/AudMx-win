from Bobla_lib.serialLib import SerCDC
from qasync import QEventLoop, asyncSlot
from PySide6.QtCore import QIODevice, Signal, QObject, QTimer
from Bobla_lib.test_py_func import MyBlye, BluetoothHandler
from enum import Enum


import asyncio


class Mod(Enum):
    BLU = 0
    SER = 1

class ConectAudMX(QObject):
    SignalSerialStartOk = Signal()
    __mod = Mod.SER
    __loop = None

    def __init__(self, loop):
        self.__loop = loop
        super(ConectAudMX, self).__init__()
        self.ser = SerCDC(True)
        self.blu = BluetoothHandler()
        # handler = BluetoothHandler()
        # asyncio.run(handler.main())
        self.ser.SignalSerialStartOk.connect(lambda: self.SignalSerialStartOk.emit())
        # self.blu.SignalBluStartOk.connect(lambda: self.SignalSerialStartOk.emit())

    def setHanglerRead(self, hangler):
        self.ser.setHanglerRead(hangler)
        # self.blu.setHanglerRead(hangler)

    def clearnSend(self):
        self.ser.clearnSend()

    def clearnQuwewe(self):
        self.ser.clearnQuwewe()

    def changMod(self):
        if self.__mod == Mod.SER:
            self.__mod = Mod.BLU
        else:
            self.__mod = Mod.SER

    @property
    def doesSerWork(self):
        if self.__mod == Mod.SER:
            return self.ser.doesSerWork
        else:
            pass
            # return self.blu.doesBluWork

    def autoConnect(self, vid, pid, buad_rate, reconnect):
        print("autoConnect")
        if self.__mod == Mod.SER:
            self.ser.autoConnect(vid, pid, buad_rate, reconnect)
        else:
            # self.blu.connect("AudMX", "00002ff3-0000-1000-8000-00805f9b34fb")
            asyncio.run(self.blu.main())

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


