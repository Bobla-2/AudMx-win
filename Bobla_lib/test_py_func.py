import asyncio
import random
import string
import threading
from bleak import BleakClient, BleakScanner
import queue
from PySide6.QtCore import QTimer, Signal, QObject
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from Bobla_lib.single_ton_meta import Singleton
import sys


glob_queue = queue.Queue()
glob_queue_tx = queue.Queue()

class MyBlue(QObject):
    SignalSerialStartOk = Signal()
    __blu_work = False
    __handleRead = None
    buff_send = ""
    tmp = ''
    def __init__(self, skjd):
        self.skjd = skjd
        global glob_queue
        self.my_queue = glob_queue
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_queue)
        self.timer.setInterval(150)
        self.__watch_dog = QTimer()
        self.__watch_dog.timeout.connect(self.__watchDog)
        self.__watch_dog.setInterval(8000)
    def __watchDog(self):
        self.__watch_dog.stop()
        self.__blu_work = False
        self.close()
        self.autoConnect("AudMX")

    def write(self, str_):
        print("write: test_f:" + str_)
        if str_[:9] == "SET_ICON ":
            self.buff_send = "00002ff" + str(int(str_[9]) + 2) + "-0000-1000-8000-00805f9b34fb"
            global glob_queue
            glob_queue.put("Send 352 bytes")
            print("glob_queue.put: Send 352 bytes")
            return

    def writeBytes(self, ast):
        print([self.buff_send, ast])
        global glob_queue_tx
        glob_queue_tx.put([self.buff_send, ast])
        self.buff_send = ""
        global glob_queue
        glob_queue.put("OK")
        self.check_queue()

    def setHanglerRead(self, hang: object):
        self.__handleRead = hang
    @property
    def doesBluWork(self):
        return self.__blu_work
    def autoConnect(self, NAME):
        self.connect(NAME)
        self.timer_con = QTimer()
        self.timer_con.timeout.connect(self.__reconnect)
        self.timer_con.setInterval(10000)
        self.timer_con.start()

    def close(self):
        global glob_queue_tx
        glob_queue_tx.put(["close"])
        self.timer_con.stop()
        self.timer.stop()
        self.__blu_work = False

    def __reconnect(self):
        if self.doesBluWork == True:
            self.timer_con.stop()
            self.timer.start()
            self.skjd()
            # self.SignalSerialStartOk.emit()
        else:
            self.__blu_work = False
            global glob_queue
            try:
                tmp = glob_queue.get_nowait()
                print("reconnect:  " + tmp)
                if tmp == "connect":
                    self.__blu_work = True
                    self.__reconnect()
                if tmp == "error: main":
                    pass
                    # self.connect("")
                elif tmp == "bluet. off":
                    if self.__handleRead and self.__handleRead != None:
                        self.__handleRead(tmp)
                    self.connect("")
                else:
                    global glob_queue_tx
                    glob_queue_tx.put(["reconnect"])
                # self.__reconnect()
            except queue.Empty:
                pass


    def connect(self, NAME):
        print("connect")
        self.__loop = asyncio.new_event_loop()

        self.__t = threading.Thread(target=self.run_in_thread, args=(self.__loop, self.my_queue,))
        self.__t.daemon = True
        self.__t.start()
        # self.__blu_work = True

    def check_queue(self):
        try:
            tmp = self.my_queue.get_nowait()
            # if tmp == "connect":

            if self.__handleRead != None:
                self.__watch_dog.start()
                print("check_queue " + tmp)
                self.__handleRead(tmp)
                self.check_queue()
            else:
                print("self.__handleRead ! None")
        except queue.Empty:
            pass
    # def write(self, str):
    #     print(str)
    #     pass

    async def notification_handler(self, sender, data):
        data_str = data.decode("utf-8")
        global glob_queue
        glob_queue.put(data_str)

    async def find_device_address(self, device_name, queue):
        try:
            devices = await BleakScanner.discover()
        except:
            queue.put("bluet. off")
            sys.exit()
            # print("bluet. off")
            return None
        for device in devices:
            if device_name == device.name:
                return device.address
        return None

    async def send_blob_chunk(self, client, characteristic_uuid, chunk):
        try:
            await client.write_gatt_char(characteristic_uuid, chunk, response=True)
            print(f"Chunk sent: {chunk}")
        except Exception as e:
            print(f"Failed to send chunk: {e}")

    async def send_blob(self, client, characteristic_uuid, blob):
        chunk_size = 200
        for i in range(0, len(blob), chunk_size):
            chunk = blob[i:i + chunk_size]
            await self.send_blob_chunk(client, characteristic_uuid, chunk)

    async def send_img(self, client, characteristic_uuid, img):
        # Отправка мусора что бы сбросить входной буффер
        chunk = "!"
        await client.write_gatt_char("00002ff1-0000-1000-8000-00805f9b34fb", chunk.encode("UTF-8"), response=True)
        print("send_img")
        characters = img
        # Рандомная хуйня что бы заплнить экран


        await self.send_blob(client, characteristic_uuid, characters)
        # await self.send_blob(client, characteristic_uuid, img)

    async def connect_and_subscribe(self, device_address, characteristic_uuid):
        global glob_queue_tx
        global glob_queue
        try:
            async with BleakClient(device_address) as client:
                if client.is_connected:
                    # Уведомления для громкости
                    await client.start_notify(characteristic_uuid, self.notification_handler)
                    # У каждого дисплея уникальный адрес, 00002ff3 - он закодирован в последней цифре, 3 - это второй диспей, 2 - первый и тд

                    # await self.send_img(client, "00002ff3-0000-1000-8000-00805f9b34fb")
                    glob_queue.put("connect")
                    print("as)")
                    while True:
                        await asyncio.sleep(0.2)
                        # print("asyncio.sleep(200)")
                        try:
                            tmp = glob_queue_tx.get_nowait()
                            # print("tmp: " + tmp)
                            if len(tmp) != 0:
                                if tmp[0] == "reconnect":
                                    pass
                                elif tmp[0][0] == "0":
                                    print("tmp: elif tmp[0][0] == 0:")
                                    await self.send_img(client, tmp[0], tmp[1])
                                elif tmp[0] == "close":
                                    sys.exit()

                        except queue.Empty:
                            pass
        except Exception as e:
            print(f"Exception: {e}")

    async def main(self, queue):
        DEVICE_NAME = "AudMX"
        CHARACTERISTIC_UUID = "00002ff0-0000-1000-8000-00805f9b34fb"
        device_address = await self.find_device_address(DEVICE_NAME, queue)
        if device_address:
            await self.connect_and_subscribe(device_address, CHARACTERISTIC_UUID)
        else:
            queue.put("error: main")
            sys.exit()

    def run_in_thread(self, loop, queue):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.main(queue))



if __name__ == "__main__":
    c = MyBlue()
    while True:
        pass
